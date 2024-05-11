import sqlite3
from colorama import init, Back, Fore, Style

class ListCompany:

    def __init__(self,db_path):        
        self.db_path = db_path
        self.contracts = []


    def getContracts(self):
         return self.contracts

    def setContracts(self, contract):
         self.contracts = contract    

    def contractQuery(self):

        try:
            # Conectar ao banco de dados SQLite
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()

            # Consulta os dados de Empresas na tabela 'company'
            cursor.execute("SELECT id,social_reason FROM company")
            found = cursor.fetchall()

            list = []

            if found:               
               self.setContracts(found)        

            # Commit da transação e fechamento da conexão
            connection.commit()
            connection.close()



        except Exception as e:
            return e    
