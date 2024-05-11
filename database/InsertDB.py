import sqlite3
import hashlib
from colorama import init, Back, Fore, Style
from database.UserQueryDB import *

class InsertDB:
    def __init__(self, db_path, user_data):
        self.db_path = db_path
        self.user_data = user_data
        self.hashed_password = None
        self.msg = None


    def getPassword(self):
        return self.hashed_password
    
    def getMsg(self):
        return self.msg

    def setPassword(self):
        # Criptografar a senha
        self.hashed_password = hashlib.sha256(self.user_data['password'].encode()).hexdigest()    

    def insert_user(self):
        try:            
            # Conectar ao banco de dados SQLite
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()    

           # Definir a tabela 'user' se ela não existir
            cursor.execute(
                '''CREATE TABLE IF NOT EXISTS dataUser (
                    cpf        TEXT,
                    password   TEXT,
                    nome       TEXT,
                    ingresso   TEXT,
                    situacao   TEXT,
                    cargo      TEXT
                )'''
            )

            # Inserir os dados do usuário na tabela 'user'
            insert_query = "INSERT INTO dataUser (cpf, password, nome, ingresso, situacao, cargo) VALUES (?, ?, ?, ?, ?, ?)"
            user_data_tuple = (self.user_data['cpf'].strip(), self.getPassword(), self.user_data['nome'].strip(), self.user_data['ingresso'].strip(), self.user_data['situacao'].strip(), self.user_data['cargo'].strip())

            cursor.execute(insert_query, user_data_tuple)


            # Commit da transação e fechamento da conexão
            connection.commit()
            connection.close()

            self.msg =  f"{Fore.BLUE}Usuário inserido com sucesso no banco de dados..{Fore.RESET}"             

        except Exception as e:
            self.msg = f"{Fore.BLUE}Error: Falha ao inserir usuário no banco de dados: {e}.{Fore.RESET}" 
            

