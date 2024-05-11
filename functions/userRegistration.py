import getpass
from database.InsertDB import *
from authentication.Connection import *
from functions.isValidPhone import *
from functions.isValidEmail import *
from functions.apiTransparencyUser import *
from dotenv import load_dotenv
import os
from colorama import init, Back, Fore, Style

def userRegistration():

    load_dotenv()

    while True:
        selected = int(input("Você quer realizar um cadastro no FIC? 1-Sim 2-Não: "))
        if selected == 2:
            print("Ótimo! Você já possui cadastro. Vamos adiante.")
            break
        elif selected == 1:
            password = ""  # Senha capturada logo abaixo
            print("Entendido! Vamos criar um novo cadastro.")
            profile = int(input("Qual seu perfil? 1-Adm ou 2-Fiscal Técnico \n"))
            if profile == 1:
                  user = input("Digite seu usuário do Zabbix. \n")
                  password = input("Digite sua senha do Zabbix. \n")
                  adm = Connection(user,password)
                  print(adm.userAdmZabbix())
                  res = adm.getMsg()
                  if res == False:
                     print("Desculpe. Vou sair do sistema. Peça ao Adm seu registro no sistema, antes de prosseguir.")
                     sys.exit()
            
            cpf  = input("Digite o número do seu CPF.(Somente números) \n")
               # Antes verifico se o usuário já existe no DB
            found = UserQueryDB(cpf,os.getenv("DB_PATH"))
            search = found.userQuery()
            
            if search == 1:
                print(f"{Fore.BLUE}Usuário já possui cadastro no DB..{Fore.RESET}")
                break            

            # Senha                    
            while True:
                password1 = getpass.getpass("Digite a senha (1 letra maiúscula, 1 número, 1 caractere especial): ")
                password2 = getpass.getpass("Repita a senha: ")

                if password1 == password2:
                    # Verifique se a senha atende aos requisitos (maiúscula, número, caractere especial)
                    if any(c.isupper() for c in password1) and any(c.isdigit() for c in password1) and any(not c.isalnum() for c in password1):
                        password = password1
                    else:
                        print("A senha deve conter pelo menos 1 letra maiúscula, 1 número e 1 caractere especial.")
                else:
                    print("As senhas não coincidem. Tente novamente.") 

                # Vou pegar mais dados do usuário baseado no CPF na API da transparencia
                user_api = api_transparencia_user_details(cpf)                        
                                         
                # Instanciar o InsertDB.py
                list_user = {                   
                    "cpf"     : cpf,                  
                    "password": password,                    
                }
                list_user.update(user_api[0])                
                db_insert = InsertDB(os.getenv("DB_PATH"),list_user) # Instancio objeto
                db_insert.setPassword() # Criptografo a senha em sha256
                db_insert.insert_user() # Executo o método de inserção no DB
                res = db_insert.getMsg() # retorno o resultado                
                if 'Error' in res:
                    print(res)
                    sys.exit()
                else:
                    print(res) 
                    sys.exit()                    
            
                break
        else:
            print("Opção inválida! Digite 1 para 'Sim' ou 2 para 'Não'.")
