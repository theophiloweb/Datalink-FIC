import sqlite3
from colorama import init, Back, Fore, Style

class UserQueryDB:

    def __init__(self,cpf,db_path):
        self.cpf = cpf
        self.db_path = db_path

    def userQuery(self):

        try:
            # Conectar ao banco de dados SQLite
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Inserir os dados do usuário na tabela 'user'
            cursor.execute("SELECT cpf FROM user WHERE cpf = ?", (self.cpf,))
            found = cursor.fetchone()

            if found:
                return 1

            # Commit da transação e fechamento da conexão
            connection.commit()
            connection.close()



        except Exception as e:
            return e    
