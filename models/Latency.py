import requests
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np
from dotenv import load_dotenv
import os
import sys

class Latency:

    def __init__(self, date_start, date_end, item):
        self.__dateStart               = date_start
        self.__dateEnd                 = date_end
        self.__item                    = item
        self.percentile_95             = 0
        self.count                     = 0
        self.min_value                 = 0
        self.occurrences_percentille95 = 0
        self.latency_occurrences       = []

    
    def getLatencyOccurrences(self):
        return self.latency_occurrences
        
    def getLatencyPercentile95(self):
        return self.percentile_95
    
    def getLatencyCount(self):
        return self.count
    
    def getMinValue(self):
        return self.min_value
    
    def getOccurrencesPercentille95(self):
        return self.occurrences_percentille95
    
    def setLatencyPercentile95(self,percentile95):
        self.percentile_95 = percentile95

    def setLatencyCount(self,count):
        self.count = count    

    def setLatencyOccurrences(self, occurrences):
        self.latency_occurrences = occurrences  

    def setMinValueLatency(self,min_value):
        self.min_value = min_value    

    def setOccurrencesPercentille95(self,occurrences_percentille95):
        self.occurrences_percentille95 = occurrences_percentille95      

    def calcLatency(self):
        load_dotenv()
        daily_averages = []

        # Ajustar os horários de início e fim do período para 00:00:00 e 23:59:59, respectivamente
        start_period = datetime.combine(self.__dateStart, datetime.min.time())
        end_period = datetime.combine(self.__dateEnd, datetime.max.time())

        # Obter os timestamps Unix para o início e fim do período
        timestamp_start_period = int(start_period.timestamp())
        timestamp_end_period = int(end_period.timestamp())


        # Dados da solicitação para obter o histórico
        data = {
            "jsonrpc": "2.0",
            "method": "history.get",
            "params": {
                "output": "extend",
                "history": 0,  # Tipo de histórico: 0 para valores numéricos
                "itemids": [self.__item],
                "time_from": timestamp_start_period,
                "time_till": timestamp_end_period,
                "limit": 100000
            },
            "auth": os.getenv("ZABBIX_API_TOKEN"),
            "id": 2
        }

        # Tentativas de obter o histórico
        num_tentativas = 3
        for tentativa in range(num_tentativas):
            response = requests.post(
                os.getenv("ZABBIX_API_URL"),
                headers={"Authorization": f"Bearer {os.getenv('ZABBIX_API_TOKEN')}"},
                json=data
            )

            if response.status_code == 200:
                # Obter o histórico e processá-lo
                history = response.json()["result"]
                daily_averages = self.process_latency_history(history)
                self.setLatencyOccurrences(daily_averages)
                self.percentil_total_values(daily_averages)
                break  # Sair do loop se a solicitação foi bem-sucedida
            else:
                print(f"Erro ao obter o histórico (tentativa {tentativa + 1}/{num_tentativas}): {response.status_code}")
                if tentativa == num_tentativas - 1:
                    print(f"Erro ao obter o histórico após {num_tentativas} tentativas. Verifique a conexão com o Zabbix.")
                    # Você pode adicionar aqui um código para lidar com o erro final, 
                    # como lançar uma exceção ou retornar um valor de erro. 

   
    def process_latency_history(self,history):
    # Inicializar um dicionário para armazenar os resultados por intervalo de 5 minutos
        interval_results = defaultdict(lambda: {'values': [], 'amount': 0})
        
        # Ordenar os resultados pelo campo 'clock'
        sorted_history = sorted(history, key=lambda x: int(x['clock']))
        
        # Iterar sobre os resultados e agrupá-los em intervalos de 5 minutos
        current_interval_start = int(sorted_history[0]['clock'])
        for item in sorted_history:
            # Verificar se o item pertence ao intervalo atual
            if int(item['clock']) < current_interval_start + 300:  # 300 segundos = 5 minutos
                interval_results[current_interval_start]['values'].append(float(item['value']))
                interval_results[current_interval_start]['amount'] += 1
            else:
                # Calcular a média das latências dentro do intervalo atual
                interval_mean = sum(interval_results[current_interval_start]['values']) / interval_results[current_interval_start]['amount']
                interval_results[current_interval_start]['value'] = round(interval_mean, 2)
                
                # Avançar para o próximo intervalo
                current_interval_start = int(item['clock'])
                interval_results[current_interval_start]['values'].append(float(item['value']))
                interval_results[current_interval_start]['amount'] += 1
                
        # Calcular a média das latências para o último intervalo, se houver
        if interval_results:
            last_interval_mean = sum(interval_results[current_interval_start]['values']) / interval_results[current_interval_start]['amount']
            interval_results[current_interval_start]['value'] = round(last_interval_mean, 2)

        # Converter defaultdict para um dicionário comum
        interval_results = dict(interval_results)    
        return interval_results
    
    def percentil_total_values(self, daily_averages):
        # Inicializar uma lista para armazenar todos os valores
        all_values = []

        # Iterar sobre cada item em daily_averages
        for item in daily_averages.values():
            # Verificar se o item possui a chave 'values'
            if 'values' in item:
                # Adicionar os valores do item à lista all_values
                all_values.extend(item['values'])

        # Calcular o percentil 95 dos valores
        percentile_95 = np.percentile(all_values, 95)

        # Contar as ocorrências de valores maiores que o percentil 95
        occurrences_percentille95 = sum(1 for valor in all_values if valor > percentile_95)

        # Obter o menor valor
        sorted_values = sorted(all_values)
        L_min = sorted_values[0]
        
        # Imprimir o total de ocorrências de valores e o percentil 95
        total_count = len(all_values)
        #print("O total de ocorrências de value é ", total_count)
        #print("O percentil 95 é ", round(percentile_95,2))

        self.setLatencyPercentile95(round(percentile_95,2))
        self.setLatencyCount(total_count)
        self.setMinValueLatency(round(L_min,2))
        self.setOccurrencesPercentille95(occurrences_percentille95)
        
   


