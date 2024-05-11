import sqlite3
from colorama import init, Back, Fore, Style

class UserData:

    def __init__(self,cpf,db_path):
        self.cpf = cpf
        self.db_path = db_path

    def userData(self):

        try:
            # Conectar ao banco de dados SQLite
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Inserir os dados do usuário na tabela 'user'
            cursor.execute("SELECT * FROM dataUser WHERE cpf = ?", (self.cpf,))
            found = cursor.fetchone()

            if found:
                return found

            # Commit da transação e fechamento da conexão
            connection.commit()
            connection.close()



        except Exception as e:
            return e    
