import sqlite3
import hashlib
from colorama import init, Back, Fore, Style
from database.UserQueryDB import *

class InsertCompanyDB:
    def __init__(self, db_path, company_data):
        self.db_path = db_path
        self.company_data = company_data  
        self.id = None      
        self.msg = None


        
    def getMsg(self):
        return self.msg  

    def getId(self):
        return self.id  
    
    def setId(self,id):
        self.id = id

    def insert_company(self):
        try:
            # Conectar ao banco de dados SQLite
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()      

             # Criar a tabela company se ela ainda não existir
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS company (
                id INTEGER PRIMARY KEY,
                cnpj TEXT,
                social_reason TEXT                                   
            )
        """)

            # Inserir os dados da empresa na tabela 'company'
            cursor.execute("INSERT INTO company (cnpj, social_reason) VALUES (?, ?)",
                        (self.company_data['fornecedor_cnpjFormatado'], self.company_data['fornecedor_nome'].upper()))

            
            # Obter o ID do último registro inserido
            self.setId(cursor.lastrowid)

            # Commit da transação e fechamento da conexão
            connection.commit()
            connection.close()

            self.msg =  f"{Fore.BLUE}Empresa inserida com sucesso no banco de dados..{Fore.RESET}"             

        except Exception as e:
            self.msg = f"{Fore.BLUE}Error: Falha ao inserir a Empresa no banco de dados: {e}.{Fore.RESET}" 
            

