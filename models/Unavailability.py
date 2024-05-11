import requests
from datetime import datetime
from dotenv import load_dotenv
import os

class Unavailability:
      def __init__(self, date_start,date_end,item):
        self.__dateStart        = date_start
        self.__dateEnd          = date_end
        self.__item              = item        
        self.unavailability      = {}
        self.msg                 = None

      def getUnavailability(self):
          return self.unavailability

      def calcUnavailabilityZabbix(self):
            load_dotenv()  
          # Dados da solicitação para obter a triggerid associada ao itemid
            data_trigger = {
                "jsonrpc": "2.0",
                "method": "trigger.get",
                "params": {
                    "output": ["triggerid"],  
                    "itemids": [self.__item],
                },
                "auth": os.getenv("ZABBIX_API_TOKEN"),
                "id": 1
            }

            # Fazer uma solicitação à API Zabbix para obter a triggerid associada ao itemid
            response = requests.post(os.getenv("ZABBIX_API_URL"), headers={"Authorization": f"Bearer {os.getenv('ZABBIX_API_TOKEN')}"}, json=data_trigger)
        
            # Processar a resposta
            if response.status_code == 200:
                # Obter a triggerid associada ao itemid
                trigger_id = response.json()["result"][0]["triggerid"]

                #  # Definir o período de tempo
                start_timestamp = int(datetime.strptime(self.__dateStart.strftime('%Y-%m-%d'), '%Y-%m-%d').timestamp())
                end_timestamp = int(datetime.strptime(self.__dateEnd.strftime('%Y-%m-%d'), '%Y-%m-%d').timestamp())

                # Dados da solicitação para obter eventos relacionados à indisponibilidade
                data_event = {
                "jsonrpc": "2.0",
                "method": "event.get",
                "params": {
                    "output": ["eventid", "objectid", "r_eventid", "clock", "name", "severity", "hostid", "value"],        
                    "triggerids": [trigger_id],
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    "time_from": start_timestamp,
                    "time_till": end_timestamp,
                },
                "auth": os.getenv("ZABBIX_API_TOKEN"),
                "id": 1
            }

                # Fazer uma solicitação à API Zabbix para obter os eventos relacionados à indisponibilidade
                response_event = requests.post(os.getenv("ZABBIX_API_URL"), headers={"Authorization": f"Bearer {os.getenv('ZABBIX_API_TOKEN')}"}, json=data_event)

                # Processar a resposta
                if response_event.status_code == 200:
                    # Obter os eventos relacionados à indisponibilidade
                    events = response_event.json()["result"]

                    # Filtrar eventos e calcular a indisponibilidade
                    availability_results = []           
                    for event in events:
                        if event['value'] == "1" and event['objectid'] == trigger_id:
                            # Verificar se há um evento relacionado (r_eventid) com o mesmo r_eventid
                            related_event = next((e for e in events if e["eventid"] == event["r_eventid"]), None)
                            if related_event:
                                # Calcular a diferença em minutos entre start_time e end_time
                                start_time = datetime.fromtimestamp(int(event["clock"]))
                                end_time = datetime.fromtimestamp(int(related_event["clock"]))
                                duration_minutes = (end_time - start_time).total_seconds() // 60

                                # Adicionar à lista de resultados apenas eventos que iniciaram e terminaram com o mesmo r_eventid
                                availability_results.append({
                                    "itemid": event["objectid"],
                                    "start_time": start_time.strftime('%d/%m/%Y %H:%M:%S'),
                                    "end_time": end_time.strftime('%d/%m/%Y %H:%M:%S'),
                                    "duration_minutes": duration_minutes
                                })


                    # Verificar se existem resultados de indisponibilidade
                    if availability_results:
                        # Exibir os resultados
                        self.unavailability = availability_results
                    else:
                        self.msg = "Nenhum evento de indisponibilidade encontrado."                        

                else:
                    self.msg = (f"Erro ao obter os eventos: {response_event.status_code}")                    

            else:
                self.msg = (f"Erro ao obter a triggerid: {response.status_code}")
                