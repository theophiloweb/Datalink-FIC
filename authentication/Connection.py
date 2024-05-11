import requests
from dotenv import load_dotenv
import os
import sys

class Connection:

    #Construtor
    def __init__(self,user,password):
       
        self.__user = user
        self.__password = password     
        self.msg = ""

    # Get dos dados instanciados 
    def getMsg(self):
        return self.msg      

    def userAdmZabbix(self): 
        load_dotenv()        
        if os.getenv("ZABBIX_API_URL"):                    
          # Código API Zabbix para busca de usuário         
          authenticate ={
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
              "user": self.__user,
              "password": self.__password
               },
            "id": 1
            }
          response = requests.post(os.getenv("ZABBIX_API_URL"), headers={"Authorization": f"Bearer {os.getenv('ZABBIX_API_TOKEN')}"}, json=authenticate)          

          try:
              if response.status_code == 200:
                  self.msg = True  
              else:
                  self.msg = False
          except ValueError:
              self.msg = "Ocorreu um erro ao se conectar com o Zabbix. Consulte o Adm do Sistema."              
                       
          finally:
              print("")
                        






