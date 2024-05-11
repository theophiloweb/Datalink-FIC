import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

class Jitter:

     def __init__(self, date_start,date_end,item):
        self.__dateStart = date_start
        self.__dateEnd   = date_end
        self.__item      = item
        self.jitter   = 0    

     def getJitter(self):
        return self.jitter   

     def calcJitZabbix(self):
        load_dotenv()
        # Criar uma lista para armazenar as médias diárias
        daily_averages = []

        # Iterar sobre cada dia no período de tempo
        for dia in range((self.__dateEnd - self.__dateStart).days + 1):
            
            # Obter a data atual
            current_date = self.__dateStart + timedelta(days=dia)

            # Definir a hora, minuto e segundo como zero para a data inicial e final do dia
            start_day = datetime(current_date.year, current_date.month, current_date.day, 0, 0, 0)
            end_day =   datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59)

            # Obter o timestamp Unix para o início e fim do dia
            timestamp_start_day = int(start_day.timestamp())
            timestamp_end_day = int(end_day.timestamp())

            # Dados da solicitação para obter o histórico
            data = {
                "jsonrpc": "2.0",
                "method": "history.get",
                "params": {
                    "output": "extend",
                    "history": 0,  
                    "itemids": [self.__item],
                    "time_from": timestamp_start_day,
                    "time_till": timestamp_end_day
                },
                "auth": os.getenv("ZABBIX_API_TOKEN"),  
                "id": 2
            }

            # Fazer uma solicitação à API Zabbix para obter o histórico
            response = requests.post(os.getenv("ZABBIX_API_URL"), headers={"Authorization": f"Bearer {os.getenv('ZABBIX_API_TOKEN')}"}, json=data)

            # Processar a resposta
            if response.status_code == 200:
                # Obter o histórico
                history = response.json()["result"]

                # Calcular a média diária se houver dados para o dia
                if history:
                    daily_average = sum([float(h["value"]) for h in history]) / len(history)
                    daily_averages.append(daily_average)

            else:
                print(f"Erro ao obter o histórico: {response.status_code}")

        # Calcular a latência total do período
        jitter_total = sum(daily_averages)

        self.jitter = jitter_total
