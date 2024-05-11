
import authentication.Connection as Connection
from art import *
import textwrap
import os
import json
from dotenv import load_dotenv

# Pacotes para CalcIndices
from models.item import *
from colorama import init, Back, Fore, Style
from dateutil import parser
from models.Latency import *
from models.Jitter import *
from models.PacketLoss import *
from models.AvailabilityPercent import *
from models.Unavailability import *
from tabulate import tabulate


from dateutil import parser
from colorama import init, Back, Fore, Style
from tqdm import tqdm
import time

#Import functions
from functions.DBConnection import *
from functions.userRegistration import *
from database.DBUserConnection import *
from database.CompanyQueryDB import *
from database.InsertCompanyDB import *
from database.InsertContractDB import *
from database.ContractQueryDB import *
from functions.isValidCNPJ import *
from functions.isValidContract import *
from database.ListCompany import *
from functions.system_presentation import *
from functions.apiTransparencyRequest import *
from functions.databaseActions import *
from functions.exit import *



def zabbix_items_colletion():

    # Variáveis dessa função GLOBAL
    global latencyItemid, jitterItemid,packetLossItemid,availabilityPercentItemid, dateStart, dateEnd, resutlLatency, resultJitter, resultPacketLoss, resultAvailabilityPercent, unavailability_list, selected_items, total_minutes_unavailability, total_minutes_period, percentage_availability, selected, latencyPercentile95, latencyCount,latencyMinValue,latencyOccurrencesPercentille95 

    contracts = ItemsZabbixContracts(os.getenv("ZABBIX_API_TOKEN"))
    contracts.showItems()
    options = contracts.getSelect()
    items = contracts.getItems()   

    if len(items) == 0:
        os.system('cls' if os.name == 'nt' else 'clear')   
        print(f"{Fore.RED}Não há itens a serem exibidos. Consulte o Administrador do Zabbix ou tente mais tarde.{Fore.RESET}\n")
        exit()
        sys.exit()    

    #SELEÇÃO DO ITEM DO CONTRATO********************************************************************************
    print(f"{Fore.MAGENTA}Selecione um Contrato: \n")

    # Número de colunas desejado
    num_items_per_row = 7  # Number of items per row
    spacing_between_items = 0  # Spacing between items (number of spaces)
    line_break = '\n'  # Line break character
    color_reset = Style.RESET_ALL  # Reset color style

    # Cores para os números (personalize como desejar)
    itemColor = [Fore.GREEN]
    itemNameColor = [Fore.YELLOW]
        
    # Loop aninhado para iterar sobre as linhas e colunas
    # Cores para números e nomes de itens
    item_number_color = Fore.GREEN  # Cor para números de itens
    item_name_color = Fore.YELLOW   # Cor para nomes de itens

    # Loop aninhado para iterar sobre linhas e colunas
    for row_index in range(0, len(options), num_items_per_row):
        for column_index in range(row_index, row_index + num_items_per_row):
            if column_index < len(options):
               # Acessando o item e formatando
               item = options[column_index]
               formatted_number = f"{column_index + 1:2}"  # Número formatado com 2 dígitos
               formatted_item = f"{item_number_color}{formatted_number}. {item_name_color}{item.rjust(spacing_between_items)}{color_reset}"

            # Imprimindo com espaçamento e cor
            print(formatted_item, end=" ")
    print(line_break)  # Quebra de linha após cada linha

    # ESCOLHA DO ITEM PELO USUÁRIO
    while True:
        try:
            escolha = int(input("Selecione o número do contrato acima: "))
            if escolha < 1 or escolha > len(options):
                print("Por favor, escolha um número válido.")
            else:
                selected = options[escolha - 1]
                selected_text = selected   
                selected_art = text2art(selected_text)
                centralized_art = textwrap.indent(selected_art, ' ' * 20)  
                print(f"{Fore.BLUE}{centralized_art}{Fore.RESET}")
                print("\n")
            # Vamos iniciar nossa lógica aqui
            # 1. Localizar os itemids do item selecionado        
                            
            for item in items:
                for key,value in item.items():                     
                    if selected in key and key.endswith("_Latencia"):
                        latencyItemid = value 
                    if selected in key and key.endswith("_Jitter"):
                        jitterItemid = value
                    if selected in key and key.endswith("_PerdaPct"):
                        packetLossItemid = value 
                    if selected in key and key.endswith("_Disponibilidade"):
                        availabilityPercentItemid = value                   
            
    #         Vamos exibir a Latencia, Jitter e Perda de Pacotes inicialmente para  fiscal
            
            dateStart = input("Data Inicial:")
            dateEnd   = input("Data Final:")
            try:
                dateStart = parser.parse(dateStart, dayfirst=True)
                dateEnd   = parser.parse(dateEnd, dayfirst=True)               
                                   
                # CLASS Latency
                with tqdm(total=100, desc="Calculando Latência e Jitter") as pbar:
                    latency                         = Latency(dateStart, dateEnd, latencyItemid)
                    latency.calcLatency()                   
                    latencyCount                    = latency.getLatencyCount()
                    latencyPercentile95             = latency.getLatencyPercentile95()  
                    latencyMinValue                 = latency.getMinValue()  
                    latencyOccurrencesPercentille95 = latency.getOccurrencesPercentille95()              
                    #result = json.dumps(latency.getLatency(), indent=4)                              
                    for i in range(50):  # Simula o progresso da operação
                        pbar.update(2)  # Atualiza a barra de progresso incrementalmente
                    #resutlLatency = "{:.2f}".format(latency.getLatency())
                    print("Calculado...")  

                # CLASS Jitter
                #with tqdm(total=100, desc="Calculando Jitter") as pbar:
                #    jitter = Jitter(dateStart, dateEnd, jitterItemid)
                #    for i in range(50):  # Simula o progresso da operação
                #        jitter.calcJitZabbix()
                #        pbar.update(2)  # Atualiza a barra de progresso incrementalmente
                #    resultJitter = "{:.2f}".format(jitter.getJitter())
                #    print("Calculado...")                    

                # CLASS PACKETLOSS
                with tqdm(total=100, desc="Calculando Perda de Pacotes") as pbar:
                    packetLoss = PacketLoss(dateStart, dateEnd, packetLossItemid)
                    for i in range(50):  # Simula o progresso da operação
                        packetLoss.calcPctZabbix()
                        pbar.update(2)  # Atualiza a barra de progresso incrementalmente
                    resultPacketLoss = "{:.2f}".format(packetLoss.getPacketLoss())
                    print("Calculado...")                   

                # CLASS AVAILABILITYPERCENT
                with tqdm(total=100, desc="Calculando Disponibilidade") as pbar:
                    availabilityPercent = AvailabilityPercent(dateStart, dateEnd, availabilityPercentItemid)
                    for i in range(50):  # Simula o progresso da operação
                        availabilityPercent.availability()
                        pbar.update(2)  # Atualiza a barra de progresso incrementalmente
                    resultAvailabilityPercent = "{:.2f}".format(availabilityPercent.getAvailabilityPercent())
                    print("Calculado...")           
                               

                #RESULTADO DOS ÍNDICES*********************************************************************                       
                # Limpa a tela   
                print("\n")         

                # Lista de resultados com suas etiquetas correspondentes
                results = [                    
                    (latencyPercentile95, "Latência"),
                    ((latencyPercentile95 - latencyMinValue), "Jitter"),                    
                    (resultPacketLoss, "Packet Loss"),
                    (resultAvailabilityPercent, "Availability Percent")
                ]

                # Calcula a largura para centralizar o conteúdo
                terminal_width = 80
                column_width = (terminal_width - 4) // len(results)  # Ajusta a largura da coluna com base no número de resultados

                # Imprime o cabeçalho com cores de fundo verde e texto branco, centralizado
                print(Back.GREEN + Fore.WHITE + Style.BRIGHT + "Resultados".center(terminal_width, " ") + Style.RESET_ALL)

                # Imprime cada resultado em sua própria coluna, centralizado e com cores de fundo verde e texto branco
                for result, label in results:
                    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + f"{label}".center(column_width, " ") + Style.RESET_ALL, end=' ')
                print()  # Adiciona uma nova linha após imprimir todas as etiquetas

                for result, _ in results:
                    print(Back.GREEN + Fore.WHITE + Style.BRIGHT + f"{result}".center(column_width, " ") + Style.RESET_ALL, end=' ')
                print()  # Adiciona uma nova linha após imprimir todos os resultados

                        
                #OCORRENCIAS DO ENLACE*****************************************************************************
                occurrences = Unavailability(dateStart, dateEnd, availabilityPercentItemid)  
                occurrences.calcUnavailabilityZabbix()
                # Obtendo a lista de ocorrências
                unavailability_list = occurrences.getUnavailability()

                # Verificando se há ocorrências para exibir
                if unavailability_list:
                # Imprimindo cabeçalhos da tabela
                    print("\n")
                    print("Ocorrências de Indisponibilidade: \n")
                    print("{:<10} {:<20} {:<20} {:<20}".format("Índice", "Início", "Fim", "Duração (minutos)"))
                    print("-" * 70)

                            # Lista para armazenar os itens selecionados pelo usuário
                    selected_items = []

                    # Iterando sobre as ocorrências e imprimindo cada uma
                    for i, occurrence in enumerate(unavailability_list, 1):
                        start_time = occurrence["start_time"]
                        end_time = occurrence["end_time"]
                        duration_minutes = occurrence["duration_minutes"]
                        print("{:<10} {:<20} {:<20} {:<20}".format(i, start_time, end_time, duration_minutes))

                    print("\n")

                    # Solicitando ao usuário que escolha os itens
                    print("Escolha os números dos itens que deseja selecionar (separados por vírgula):")
                    selected_indices = input(">> ").strip().split(",")

                    # Convertendo os números selecionados para índices inteiros
                    selected_indices = [int(index.strip()) for index in selected_indices if index.strip().isdigit()]

                    # Verificando se os índices selecionados são válidos e adicionando os itens selecionados à lista de itens
                    for index in selected_indices:
                        if 1 <= index <= len(unavailability_list):
                            selected_items.append(unavailability_list[index - 1])

                    #Verifica se há itens selecionados
                    if selected_items:
                                # Cria uma lista de listas com os dados dos itens selecionados
                        items_table = [[i + 1, item["start_time"], item["end_time"], item["duration_minutes"]] for i, item in enumerate(selected_items)]

                        # Define os cabeçalhos da tabela
                        os.system('cls' if os.name == 'nt' else 'clear')   
                        headers = ["Índice", "Início", "Fim", "Duração (minutos)"]
                        # Imprime a tabela formatada
                        print("\nVocê escolheu os seguintes itens:")
                        print(tabulate(items_table, headers=headers, tablefmt="fancy_grid"))
                       
                        # Variável para armazenar a soma dos minutos de indisponibilidade selecionados pelo usuário
                        total_minutes_unavailability  = 0
                        # Iterando sobre os itens selecionados pelo usuário
                        for item in selected_items:
                        # Capturando o valor de "duration_minutes" de cada item e somando
                            total_minutes_unavailability += item["duration_minutes"]
                        # Calculando o tempo total em minutos do período selecionado pelo usuário
                        total_minutes_period = (dateEnd - dateStart).total_seconds() // 60
                         #Vamos exibir o percentual de disponibilidade do Enlace segundo o contrato
                        print('Vou exibir a disponibilidade do Enlace segundo o contrato -> ((To - Ti)/To)*100')
                        resultAvailabilityPercent = ((total_minutes_period - total_minutes_unavailability)/total_minutes_period) * 100
                        # Calculando o novo percentual de disponibilidade
                        if total_minutes_period > 0:
                             percentage_availability = ((total_minutes_period - total_minutes_unavailability) / total_minutes_period) * 100
                        else:
                             percentage_availability = 0
                        # Exibindo os resultados com formatação elegante
                        print(f"{Fore.CYAN}Total de minutos de indisponibilidade selecionados:{Fore.RESET} {total_minutes_unavailability} minutos")
                        print(f"{Fore.CYAN}Tempo total do período selecionado:{Fore.RESET} {total_minutes_period} minutos")
                        print(f"{Fore.CYAN}Percentual de disponibilidade segundo o contrato:{Fore.RESET} {resultAvailabilityPercent:.2f}%")
                        print(f"{Fore.CYAN}Novo percentual de disponibilidade:{Fore.RESET} {percentage_availability:.2f}%")

                        # Determine o caminho completo para o arquivo JSON
                        json_path = os.path.join('json', 'variables.json')
                        # Converta as datas para strings antes de salvar no JSON
                        dateStart_str = dateStart.strftime('%d-%m-%Y %H:%M:%S')
                        dateEnd_str = dateEnd.strftime('%d-%m-%Y %H:%M:%S')

                        config = {
                            'latencyItemid':latencyItemid,
                            'jitterItemid':jitterItemid,
                            'packetLossItemid':packetLossItemid,
                            'availabilityPercentItemid':availabilityPercentItemid,
                            'dateStart':dateStart_str,
                            'dateEnd':dateEnd_str,                            
                            'latencyCount': latencyCount,
                            'latency': latencyPercentile95,
                            'latencyOccurrencesPercentille95': latencyOccurrencesPercentille95,
                            'jitter': (latencyPercentile95 - latencyMinValue),
                            'resultPacketLoss':resultPacketLoss,
                            'resultAvailabilityPercent':resultAvailabilityPercent,
                            'unavailability_list':unavailability_list,
                            'selected_items':selected_items,
                            'total_minutes_unavailability':total_minutes_unavailability,
                            'total_minutes_period':total_minutes_period,
                            'percentage_availability':percentage_availability,
                            'selected':selected
                        }

                        with open(json_path, 'r+') as f:
                             f.truncate(0)  # Apagar o conteúdo do arquivo
                             json.dump(config, f)

                        # Salve as variáveis em um arquivo JSON
                        with open(json_path, 'w') as f:
                            json.dump(config, f)   

                    else:
                        print("\nNenhum item selecionado.")  

                else:
                    print("Nenhuma ocorrência de indisponibilidade encontrada.")  
                
                    #ERRO CASO A DATA INFORMADA NÃO SEJA VÁLIDA**********************************************************   
            except ValueError:
                    print("Data inválida")                  
            break
        except ValueError:
                print("Por favor, digite um número.")  