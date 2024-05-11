import sqlite3
from colorama import init, Back, Fore, Style

class CompanyQueryDB:

    def __init__(self,cnpj,db_path):
        self.cnpj = cnpj
        self.db_path = db_path
        self.msg = None

    def getMsg(self):
        return self.msg

    def setMsg(self, msg):
        self.msg = msg    

    def companyQuery(self):

        try:
            # Conectar ao banco de dados SQLite
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Inserir os dados do usuário na tabela 'user'
            cursor.execute("SELECT cnpj FROM company WHERE cnpj = ?", (self.cnpj,))
            found = cursor.fetchone()

            if found:
                return 1
            else:
                self.setMsg("Empresa ainda não consta no DB. Vou adicionar.")

            # Commit da transação e fechamento da conexão
            connection.commit()
            connection.close()



        except Exception as e:
            return e    
