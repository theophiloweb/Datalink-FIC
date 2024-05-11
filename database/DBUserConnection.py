from dotenv import load_dotenv
import os
from art import *
import textwrap
from colorama import init, Back, Fore, Style
import sqlite3
import getpass
import hashlib

class UserConnection:

    def __init__(self,login,password):
        self.__login = login
        self.__password = password

    def getLogin(self):
        return self.__login

    def getPassword(self):
        return self.__password   
    
    def setLogin(self,login):
        self.__login = login

    def setPassword(self,password):
        self.__password =  hashlib.sha256(password.encode()).hexdigest()    

    def DBUserConnection(self):
        load_dotenv()        
        try:
            # Conectar ao banco de dados SQLite
            connection = sqlite3.connect(os.getenv("DB_PATH"))
            cursor = connection.cursor()

            # Variável para contar as tentativas
            tentativas = 0

            while tentativas < 3:
                # Solicitar o login e senha do usuário                
                cursor.execute("SELECT * FROM dataUser WHERE cpf=? AND password=?", (self.getLogin(), self.getPassword()))
                user = cursor.fetchone()

                if user:
                    columns = [column[0] for column in cursor.description]
                    # Criar um dicionário com os nomes das colunas como chaves e os valores correspondentes
                    user_dict = dict(zip(columns, user))        
                    return user_dict
                else:
                    print(f"{Fore.RED}Falha na autenticação: usuário ou senha incorretos..{Fore.RESET}")                 
                    tentativas += 1
                    login = input("Digite o CPF novamente: ")
                    self.setLogin(login)
                    password = getpass.getpass("Digite a senha novamente: ")
                    self.setPassword(password)

            # Se exceder o limite de tentativas
            print(f"{Fore.RED}Limite de tentativas excedido. Saindo do sistema.{Fore.RESET}")          
            return False

        except Exception as e:
            print(f"{Fore.RED}Falha na autenticação: {e}.{Fore.RESET}")
            return False

        finally:
            # Fechar a conexão com o banco de dados
            if connection:
                connection.close()


