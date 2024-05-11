from colorama import Fore, Style  # Cores e estilos
from prettytable import PrettyTable
import math
import locale

def gloss_pct_loss(pctloss, value_month, incidence):
    # Definir o limiar de qualidade
    quality_threshold = 1

    # Inicializar a string de saída
    output_string = ""

    # Cabeçalho
    output_string += Fore.BLUE + Style.BRIGHT + "Cálculo da Glosa da Perda de Pacotes" + Style.RESET_ALL + "\n"

    # Fórmula
    output_string += Fore.YELLOW + "Fórmula:" + Style.RESET_ALL + "\n"
    output_string += Fore.MAGENTA + "G = (((TPPm / 100) - (TPPl / 100)) / 0.02) * d * C" + Style.RESET_ALL + "\n"

    # Tabela de variáveis (inicialmente vazia)
    tabela = PrettyTable()
    tabela.field_names = ["Variável", "Valor"]

    # Inicializar 'discount' com um valor padrão
    discount = 0  

    # Calcular o número de intervalos de 2% excedidos
    excess_intervals = math.ceil((pctloss - quality_threshold) / 0.02) 

    # Definir os descontos baseados na incidência
    if incidence == 2:
        if pctloss <= 5 and pctloss > quality_threshold:
            discount = 0.05 * excess_intervals  
        elif pctloss > 5:
            discount = 0.1 * excess_intervals  
    elif incidence == 3:
        if pctloss <= 5 and pctloss > quality_threshold:
            discount = 0.1 * excess_intervals  
        elif pctloss > 5:
            discount = 0.15 * excess_intervals  
    elif incidence == 4:
        if pctloss <= 5 and pctloss > quality_threshold:
            discount = 0.15 * excess_intervals  
        elif pctloss > 5:
            discount = 0.2 * excess_intervals  
    else:
        discount = 0  # Sem desconto para outras incidências

    # Calcular a glosa considerando o número de ocorrências
    gloss = (((pctloss/100) - (quality_threshold/100)) / 0.02) * discount * value_month

    # Popular a tabela com os valores
    tabela.add_row(["TTPm", f"{pctloss} %"])
    tabela.add_row(["TTPl", f"{quality_threshold} %"])
    tabela.add_row(["d", discount])
    tabela.add_row(["C", f"R$ {value_month}"])

    # Adicionar a tabela à string de saída
    output_string += str(tabela) + "\n"
    output_string += Fore.YELLOW + "Resultado:" + Style.RESET_ALL + "\n"
    # Cálculo da glosa
    output_string += Fore.GREEN + f"G = {locale.currency(gloss, grouping=True, symbol=False)}" + Style.RESET_ALL

    return output_string, gloss