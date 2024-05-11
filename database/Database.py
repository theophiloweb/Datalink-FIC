import sqlite3
import os
import sys
from dotenv import load_dotenv
from colorama import init, Back, Fore, Style

load_dotenv()  # Iniciar DntEnv

class Database:
    def __init__(self, db_path):
        self.db_path = db_path

    def connect(self):
            try:
                # Verifica se o arquivo do banco de dados existe
                if not os.path.exists(self.db_path):
                    return 1  # Arquivo do banco de dados não encontrado
                
                # Conectar ao banco de dados SQLite
                self.connection = sqlite3.connect(self.db_path)
                self.cursor = self.connection.cursor()

                # Verificar se a tabela já existe
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
                table_exists_user = self.cursor.fetchone()
                self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='contractor'")
                table_exists_contractor = self.cursor.fetchone()

                # Se a tabela de usuário não existir, crie-a
                if not table_exists_user:
                    self.cursor.execute("CREATE TABLE user (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, cpf TEXT, email TEXT, pg TEXT, password TEXT, phone TEXT)")
                    self.connection.commit()                
                
                # Se a tabela de contratante não existir, crie-a e insira os dados
                if not table_exists_contractor:
                    self.cursor.execute("CREATE TABLE contractor (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, cod INTEGER)")
                    self.connection.commit()

                    self.cursor.execute("INSERT INTO contractor (name, cod) VALUES (?, ?)", (os.getenv("UNIDADE_GESTORA_NAME"), os.getenv("UNIDADE_GESTORA_COD")))
                    self.connection.commit()

                return 3  # Tabelas criadas e dados inseridos com sucesso

            except sqlite3.Error as e:
                # Se houver uma exceção, defina a conexão e o cursor como None e retorne uma mensagem de erro
                self.connection = None
                self.cursor = None
                return f"{Fore.RED}Falha na conexão com o banco de dados: {e}.{Fore.RESET}"

            


            

    def close(self):
        if self.connection:
            self.connection.close()
            return f"{Fore.YELLOW}Conexão com o banco de dados fechada.{Fore.RESET}"  
            



