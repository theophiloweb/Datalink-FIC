import authentication.Connection as Connection
import requests
import os
import json
from dotenv import load_dotenv
import getpass
from docx import Document
from art import *
import textwrap
import sys

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
from prettytable import PrettyTable
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
from database.UserData import *
from models.IA import *
from functions.isValidCNPJ import *
from functions.isValidContract import *
from database.ListCompany import *
from functions.system_presentation import *
from functions.apiTransparencyRequest import *
from functions.apiTransaparencyDetailsContract import *
from functions.databaseActions import database_actions, selected_contract
from functions.apiTransparencyUser import *
from functions.zabbixItemsColletion import zabbix_items_colletion
from functions.zabbixItemsColletion import *
from functions.loginSystem import *
from functions.success import *
from functions.selectOptionIndexAvailability import *
from functions.glossAvailability import *
from functions.glossLatency import *
from functions.glossJitter import *
from functions.glossPctLoss import *
from functions.providerIndicators import *
from functions.generateReport import *

load_dotenv()  # Iniciar DntEnv

#Inciar a instância da IA
ia = IAInteraction()
ia.start_chat()

#Variáveis Gobais que estão dentro de escopo if/else
result_gloss_availability = None
gloss_availability_numeric = None
result_gloss_latency = None
result_gloss_jitter = None
gloss_latency_numeric = 0
gloss_jitter_numeric = 0
result_gloss_pct = 0
gloss_pct_numeric = 0



# Chamada da função para apresentar o sistema
system_presentation()
#Conexão com DB
print(DBConnection())
# Inserir usuário no DB - Perfil Administrador
userRegistration()
# Autenticação do Usuário no Sistema
response = login()
os.system('cls' if os.name == 'nt' else 'clear')   
sucess()

# Vou fazer uma conexão com DB para pegar os dados do Usuário autenticado
user_data = UserData(response['cpf'], os.getenv('DB_PATH'))
user_db = user_data.userData()

# Dados Usuário Logado na Tela
user = (    
    f"{Fore.MAGENTA}P/G: {Fore.RESET}{user_db[5]}\n"
    f"{Fore.MAGENTA}Situação: {Fore.RESET}{user_db[4]}\n"
    f"{Fore.MAGENTA}Nome: {Fore.RESET}{user_db[2]}\n"
    f"{Fore.MAGENTA}CPF: {Fore.RESET}{user_db[0]}\n"
    f"{Fore.MAGENTA}Data de Ingresso: {Fore.RESET}{user_db[3]}\n"
   
)
centralized_user = textwrap.indent(user, ' ' * 43)
print(centralized_user)
print()


# Exibir os índices dos items Contratuais do Zabbix
zabbix_items_colletion()

json_variables  = os.path.join('json', 'variables.json')
with open(json_variables) as f:
     config_variables = json.load(f)


#os.system('cls' if os.name == 'nt' else 'clear')   
# Valida O CNPJ solicitado pela função acima
cnpj = isValidCNPJ()
# Fazer uma consulta API em busca de contratos sob o CNPJ informado
selected_keys = api_transparencia_request(cnpj)
os.system('cls' if os.name == 'nt' else 'clear')   
# Popular o DB com os dados do Contrato
database_actions(selected_keys, config_variables['selected'])
# Carregue as variáveis do arquivo JSON
json_contract   = os.path.join('json', 'contract.json')  
with open(json_contract) as f:
     config_contract = json.load(f)
# Fazer uma consulta API em busca de dados detalhados do contrato selecionado
contract_details = api_transparencia_details(config_contract['id'])

#text = f"""
#       ## Detalhes dos contratos
#       *** Contratos detalhes: {contract_details}
#       Ao receber essa list em json dos dados de contratos sob a responsabilidade do CNPJ {cnpj} direto no portal da transparência do #governo federal via api token, o quê você pode falar de maneira sucinta e reduzida e direta sobre esses contratos e aqueles que estão #relacionados a enlace de dados e sob a a gerência de seus links em Fortaleza-CE.
#       """

#response = ia.send_message(text)
#print(f"IA: {response}")
#print()

#Vou tentar pegar a velocidade contratada
occurrence_found = re.search(r'\b(?!8)(\d+)\b', contract_details[0]['descComplementarItemCompra'])
# Verificar se a ocorrência foi encontrada
if occurrence_found:
    speed_found = occurrence_found.group(0)    
else:
    speed_found = 'Não definida'
 
# Limpa a tela
os.system('cls' if os.name == 'nt' else 'clear')   
dashboard = (    
    f"{Fore.MAGENTA}Contratante: {Fore.RESET} {config_contract['unidadeGestora_nome']}\n"       
    f"{Fore.MAGENTA}Contrato: {Fore.RESET} {config_variables['selected']} = {config_contract['numero'].lstrip('0')}\n" 
    f"{Fore.MAGENTA}Descrição: {Fore.RESET} {contract_details[0]['descricao']}\n" 
    f"{Fore.MAGENTA}Objeto: {Fore.RESET} {contract_details[0]['descComplementarItemCompra']}\n" 
    f"{Fore.MAGENTA}Velocidade: {Fore.RESET} {speed_found}\n"   
    f"{Fore.MAGENTA}ID transparencia: {Fore.RESET} {config_contract['id']}\n"   
    f"{Fore.MAGENTA}Empresa: {Fore.RESET} {config_contract['fornecedor_nome']}\n"  
    f"{Fore.MAGENTA}CNPJ: {Fore.RESET} {config_contract['fornecedor_cnpjFormatado']}\n"
    f"{Fore.MAGENTA}Valor Mensal: {Fore.RESET} {round(float(config_contract['valorFinalCompra']) / 12, 2)}\n" 
    f"{Fore.MAGENTA}Data Prevista Término: {Fore.RESET} {datetime.strptime(config_contract['dataFimVigencia'], '%Y-%m-%d').strftime('%d/%m/%Y')}\n"      
    f"{Fore.MAGENTA}Latência - Percentille95: {Fore.RESET}{config_variables['latency']} ms\n"
    f"{Fore.MAGENTA}Latência - Número de Incidências P95Lnm: {Fore.RESET}{config_variables['latencyOccurrencesPercentille95']}\n"
    f"{Fore.MAGENTA}Jitter Zabbix: {Fore.RESET}{config_variables['jitter']} ms\n"
    f"{Fore.MAGENTA}Perda de Pacotes Zabbix: {Fore.RESET}{config_variables['resultPacketLoss']}%\n"
    f"{Fore.MAGENTA}Disponibilidade Zabbix: {Fore.RESET}{round(float(config_variables['resultAvailabilityPercent']), 2)}%\n"
    f"{Fore.MAGENTA}Tempo total disponibilidade do Enlace(Minutos): {Fore.RESET}{config_variables['total_minutes_period']}\n"
    f"{Fore.MAGENTA}Tempo selecionado de indisponibilidade do Enlace(Minutos): {Fore.RESET}{config_variables['total_minutes_unavailability']}\n"
    f"{Fore.MAGENTA}Indisponibilidade apurada: {Fore.RESET}{round(config_variables['percentage_availability'],2)}\n"    
)

# Centralize e imprima os dados do usuário
centralized_dashboard = textwrap.indent(dashboard, ' ' * 20)
print(centralized_dashboard)

print()

# índice do Contrato [97 ou 99]
index_contract = select_option_index_availability()

os.system('cls' if os.name == 'nt' else 'clear')   

print(centralized_user)

# Glosa da Disponibilidade *******************************************************************

# Vou perguntar qual a incidencia podendo ser 1,2 e 3
incidence = int(input('Qual a incidência da ocorrência de indisponibilidade? Ex[1,2,3] \n'))
if incidence == 1:
     msg = 'Caro Provedor, houve ocorrências para glosa, mas pelo fato de ser a primeira , não haverá ,para o período, nenhuma sanção.'
     print(f"{Fore.GREEN}{msg}{Fore.RESET}") 
     

elif config_variables['percentage_availability'] >= index_contract:
     msg = 'Caro provedor, nosso índice calculado de disponibilidade de seu Enlace foi superior ao índice contratado. Parabéns.'
     print(f"{Fore.GREEN}{msg}{Fore.RESET}") 

else:
     result_gloss_availability, gloss_availability_numeric =  gloss_availability(index_contract,round(config_variables['percentage_availability'],2), round(float(config_contract['valorFinalCompra']) / 12, 2),incidence)
   
     print(result_gloss_availability)
     print(gloss_availability_numeric)

# Glosa da Latência*******************************************************************

# Vou perguntar qual a incidencia podendo ser 1,2,3 ou 4
incidence_latency = int(input('Qual a incidência de ocorrência da Latência? Ex[1,2,3,4]'))
if incidence_latency == 1:
     msg = 'Caro Provedor, houve ocorrências para glosa, mas pelo fato de ser a primeira , não haverá ,para o período, nenhuma sanção.'
     print(f"{Fore.GREEN}{msg}{Fore.RESET}") 

elif config_variables['latency'] <= 150:
     msg = 'Caro provedor, nosso índice calculado de latência de seu Enlace foi inferior ou igual ao índice contratado. Parabéns.'
     print(f"{Fore.GREEN}{msg}{Fore.RESET}") 

else:
     result_gloss_latency, gloss_latency_numeric = gloss_latency(round(config_variables['latency'],2), round(float(config_contract['valorFinalCompra']) / 12, 2),incidence_latency, config_variables['latencyOccurrencesPercentille95'])  
       
     print(result_gloss_latency)
     print(gloss_latency_numeric)

# Glosa da Jitter*******************************************************************

# Vou perguntar qual a incidencia podendo ser 1,2,3 ou 4
incidence_jitter = int(input('Qual a incidência de ocorrência de Jitter? Ex[1,2,3,4]'))
if incidence_jitter == 1:
     msg = 'Caro Provedor, houve ocorrências para glosa, mas pelo fato de ser a primeira , não haverá ,para o período, nenhuma sanção.'
     print(f"{Fore.GREEN}{msg}{Fore.RESET}") 

elif config_variables['jitter'] <= 30:
     msg = 'Caro provedor, nosso índice calculado de Jitter de seu Enlace foi inferior ou igual ao índice contratado. Parabéns.'
     print(f"{Fore.GREEN}{msg}{Fore.RESET}") 

else:
     result_gloss_jitter, gloss_jitter_numeric = gloss_jitter(round(config_variables['jitter'],2), round(float(config_contract['valorFinalCompra']) / 12, 2),incidence_jitter, config_variables['latencyOccurrencesPercentille95'])  

     print(result_gloss_jitter)    
     print(gloss_jitter_numeric) 

# Glosa da Perda de Pacotes*******************************************************************

# Vou perguntar qual a incidencia podendo ser 1,2,3 ou 4
incidence_pct_loss = int(input('Qual a incidência de ocorrência de Perda de Pacotes? Ex[1,2,3,4]'))
if incidence_pct_loss == 1:
     msg = 'Caro Provedor, houve ocorrências para glosa, mas pelo fato de ser a primeira , não haverá ,para o período, nenhuma sanção.'
     msg = Fore.GREEN + Style.BRIGHT + msg + Style.RESET_ALL + "\n"
     print(msg)

elif float(config_variables['resultPacketLoss']) <= 1.0:
     
     msg = 'Caro provedor, nosso índice calculado de perda de pacotes de seu Enlace foi inferior ou igual ao índice contratado. Parabéns.'
     msg = Fore.GREEN + Style.BRIGHT + msg + Style.RESET_ALL + "\n"
     print(msg)

else:
     result_gloss_pct, gloss_pct_numeric = gloss_pct_loss(round(float(config_variables['resultPacketLoss']), 2), 
                           round(float(config_contract['valorFinalCompra']) / 12, 2),
                           incidence_pct_loss)   
     print(result_gloss_pct) 
     print( gloss_pct_numeric)

# Vou pegar os indicadores do Provedor
provider_indicators = provider_indicators()   

# Vamos receber uma análise dos indicadores da OM e Provedor pela IA

text = f"""

     ***Atuação: Aja como um analista especialista em redes de dados. Sua análise é minuciosa e direta. Você não toma partido quando se trata de fiscalização técnica de contratos. Sua ênfase sempre será levar em consideração as melhores práticas, bom uso dos recursos públicos e um enlace disponível e que cumpre com eficácia, até certo, sua finalidade, dentro do período considerado.
     
     **Pergunta: Os indicadores da empresa contratada foram superiores ao da contratante com pouco diferença.
     **Resposta: Além das análises abaixo se adiciona a conclusão que os indicadores da empresa será utilizados para fins de glosa.


     **Pergunta:

     ## Análise de Indicadores de Desempenho de Enlace

     **Unidade Gestora:** {config_contract['unidadeGestora_nome']}
     **Enlace:** {config_variables['selected']} ({config_contract['numero'].lstrip('0')})
     **Fornecedor:** {config_contract['fornecedor_nome']}
     **Fiscal técnico de contrato atual:** {user_db[5]} {user_db[2]}
     **Objeto do Contrato:** {contract_details[0]['descComplementarItemCompra']}
     **Data prevista para término do Contrato:** {datetime.strptime(config_contract['dataFimVigencia'], '%Y-%m-%d').strftime('%d/%m/%Y')}
     **Quantidade de ocorrências de Percentille95** {config_variables['latencyOccurrencesPercentille95']}
     **Velocidade do Enlace** {config_variables['latencyOccurrencesPercentille95']} MB
     **Data inicial para coleta no Zabbix** {config_variables['dateStart']}
     **Data final para coleta no Zabbix** {config_variables['dateEnd']}
     

     Este relatório apresenta uma análise dos indicadores de desempenho do enlace, comparando os dados coletados pelo Zabbix do 52º Centro de Telemática com os indicadores fornecidos pelo provedor. O objetivo é identificar possíveis problemas de desempenho e recomendar ações corretivas.

     **Metodologia:**

     * **Latência:** A latência é medida em milissegundos (ms) e calculada usando a fórmula L = RTT / 2, onde RTT é o tempo de ida e volta. O percentil 95 das medições de latência é utilizado para avaliação. 
     * **Jitter:** O jitter representa a variação no tempo de atraso dos pacotes e é calculado como J = P95(Ln) - Lmin, onde P95(Ln) é o percentil 95 da latência e Lmin é a menor latência observada.
     * **Perda de Pacotes:** A perda de pacotes é medida como uma porcentagem do total de pacotes enviados que não chegaram ao destino. A fórmula utilizada é TPP = ((NPorigem - NPdestino) / NPorigem) * 100.
     * **Disponibilidade:** A disponibilidade é a porcentagem de tempo em que o serviço esteve operacional durante o período de análise. A fórmula utilizada é D = ((To - Ti) / To) * 100, onde To é o tempo total de operação e Ti é o tempo de indisponibilidade.

     **Limiares Contratuais:**

     | Indicador | Limiar |
     |---|---|
     | Latência (P95) | 150ms |
     | Jitter | <= 30ms |
     | Perda de Pacotes | <= 1% |
     | Disponibilidade | {index_contract} |

     **Resultados:**

     | Indicador | Zabbix | Provedor |
     |---|---|---|
     | Latência (P95) | {config_variables['latency']}ms | {provider_indicators[0]}ms |
     | Jitter | {config_variables['jitter']}ms | {provider_indicators[1]}ms |
     | Perda de Pacotes | {config_variables['resultPacketLoss']}% | {provider_indicators[2]}% |
     | Disponibilidade | {round(config_variables['percentage_availability'],2)}% | {provider_indicators[3]}% |

     **Análise e Recomendações:**

     * ** Sempre se dirija ao fiscal técnico de contrato atual.

     * **Comparação dos Dados:** Compare os resultados do Zabbix com os dados do provedor para cada indicador usando tabela formatada e legível. Não entre no mérito se existe erros nas medições, leve sempre pelo lado que ambos os lados realizaram suas medições e em príncipio está certos para cada um dos lados, sua análise será sobre os valores apurados e suas consequências para mabos os lados no que se refere a possíveis sanções e melhorias nos enlaces. Atue como especialista em redes de dados para tomar a orientações acertadas para mabos os lados. Cite a quantidade de ocorrências de percentille95 detectadas e sua aplicação no contrato se for o caso. Identifique discrepâncias significativas que possam indicar problemas de medição ou desempenho real da rede.
     * **Análise de Impacto:** Explique as potenciais consequências de exceder os limites contratuais para os indicadores que utrapassaram o limiar, e cite aqueles que mantiveram a meta, como degradação da qualidade de áudio e vídeo em videoconferências, lentidão na transmissão de dados e interrupções no serviço. Faça também uma análise sobre a distancia que engloba esse Enlace no item Objeto do Contrato, pois dependendo da cidade e distância poderá haver problemas de comunicação e interferência nos indicadores.
     * **Importância Estratégica:** Enfatize a importância do enlace para as operações da unidade militar, considerando sua função de telemática e as conexões com outras unidades. Faça também uma análise se a velocidade contrata no item em Velocidade do Enlace é viável para operação do link.
     * **Recomendações:** Com base na análise, sugira medidas corretivas que beneficiem o provedor, a menos que haja uma diferença substancial entre os dados, caso em que se deve optar pelo cenário mais favorável ao desempenho do enlace.

     **Observações:**

     * Descontos serão aplicados para cada ocorrência de P95(Ln) acima do limite de latência e jitter, e para cada 2% ou fração acima do limite de perda de pacotes.
     * Se todos os indicadores estiverem dentro dos limites contratuais, parabenize o provedor pelo cumprimento das metas. 
     * Exiba o percentual de recomendação dessa empresa contratada baseado no reclame aqui. Exiba somente o percentual de recomendação no formato: Empresa recomendada: Percentual capturado do site reclame aqui até a dataque você possui acesso.
     * É possível que os dados da contratante e contratada referente aos indicadores possam está discrepantes, se o resultado foi muito maior na comparação, devido a uso de sistemas de medição diferentes.  
     * Cite também o período de coleta e tempo de ralização em minutos.

     **Apresentação dos Resultados:**

     Os resultados da análise e as recomendações devem ser apresentados em um formato claro e conciso, utilizando sempre que possível tabelas e fontes legíveis para usuário. 

     **Objetivo:**

     O objetivo desta análise é auxiliar na garantia da qualidade do serviço de enlace, identificando e corrigindo problemas de desempenho que possam afetar as operações da unidade militar.

     ***resposta:
"""

response = ia.send_message(text)
print(f"IA: {response}")

sys.exit()

print("Agora vou gerar o relatório...")



write_report_data(config_contract['numero'].lstrip('0'),config_variables['dateStart'], contract_details[0]['descComplementarItemCompra'],config_contract['unidadeGestora_nome'], config_contract['fornecedor_nome'], config_contract['fornecedor_cnpjFormatado'],index_contract,round(config_variables['percentage_availability'],2), config_variables['resultPacketLoss'],config_variables['latency'],config_variables['jitter'], provider_indicators[3],provider_indicators[1],provider_indicators[0],provider_indicators[1],incidence,incidence_pct_loss, incidence_latency,incidence_jitter, gloss_availability_numeric, gloss_pct_numeric, gloss_latency_numeric, gloss_jitter_numeric, round(float(config_contract['valorFinalCompra']) / 12, 2), result_gloss_availability, result_gloss_latency, result_gloss_jitter, result_gloss_pct, user_db[2],user_db[5])




 
              




