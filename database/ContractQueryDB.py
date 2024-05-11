import sqlite3
from colorama import init, Back, Fore, Style

class ContractQueryDB:

    def __init__(self,contract_alias,db_path):
        self.contract_alias = contract_alias
        self.db_path = db_path
        self.msg = None

    def getMsg(self):
        return self.msg  

    def setMsg(self, msg):
        self.msg = msg  

    def contractQuery(self):

        try:
            # Conectar ao banco de dados SQLite
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Consultar na tabela 'contract'
            cursor.execute("SELECT contract_alias FROM contract WHERE contract_alias = ?", (self.contract_alias,))
            found = cursor.fetchone()

            if found:
                return 1
            else:
                self.setMsg("Contrato não existe no DB. Vamos prosseguir.")

            # Commit da transação e fechamento da conexão
            connection.commit()
            connection.close()



        except Exception as e:
            return e    
