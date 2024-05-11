import requests
import re
from dotenv import load_dotenv
import os

load_dotenv()    

class ItemsZabbixContracts:

    #Construtor
    def __init__(self,token): 
        self.item = [] # Nosso item        
        self.token = token        
        self.objects = {}
        self.contracts = []
        self.select = []
        self.option = []

    def getItems(self):  
        return self.contracts
    
    def getSelect(self):
        return self.select

    def setItem(self,name,item):
         newObjects = self.objects[name] = item
         self.item.append(newObjects)

    def showItems(self):   
           
        # Dados da solicitação para o método item.get
        data = {
            "jsonrpc": "2.0",
            "method": "item.get",
            "params": {
                "output": ["itemid", "name"], 
                "search": {"name": "Enlace"}, 
                "filter": {
                "hostids": [os.getenv("HOSTID_CORE"), os.getenv("HOSTID_CTA"), os.getenv("HOSTID_CITEX"), os.getenv('LINK_BRISANET')],
                }                
            },
            "auth": os.getenv("ZABBIX_API_TOKEN"),
            "id": 1
        }

        
        # Fazer uma solicitação à API Zabbix para obter os itens
        response_items = requests.post(os.getenv("ZABBIX_API_URL"), headers={"Authorization": f"Bearer {os.getenv('ZABBIX_API_TOKEN')}"}, json=data)
        
        # Processar a resposta
        if response_items.status_code == 200:
            items_data = response_items.json().get("result", [])  
            
            # Variavel temporária para armazenar os items do contrato
            firstFilter = []              
            
            for item in items_data:
                if re.search(r"_Disponibilidade|_Jitter|_Latencia|_PerdaPct", item["name"]) and "Alta" not in item["name"] and not item["name"].endswith("_P"):
                    firstFilter.append({"itemid": item["itemid"], "name": item["name"]})  # APrimeiro filtro nos contratos
            

            # Daqui extraimos os contratos           
            for item in firstFilter:  
                str = item['name']
                parts = str.split()
                result = parts[1]                                                          
                if result in item['name']:
                  self.objects[item['name']] = item['itemid'] 
                  self.option.append(result)
            self.contracts.append(self.objects)  

            #Daqui extraio os itens do option select
            for s in self.option: 
                s = s.replace('_Disponibilidade','').replace('_Jitter','').replace('_Latencia','').replace('_PerdaPct','')          
                self.select.append(s)   

            # Vou remover itens duuplicados em nosso select
            listDuplicates = set(self.select)
            nonDuplicateList = list(listDuplicates)
            self.select = nonDuplicateList

                        

           
            

    
