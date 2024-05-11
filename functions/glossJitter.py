from colorama import Fore, Style  # Cores e estilos
from prettytable import PrettyTable
import locale

def gloss_jitter(jitter, value_month, incidence, latency_occurrences_percentile_95):
    # Definir o limiar de qualidade
    quality_threshold = 30

    # Inicializar a string de saída
    output_string = ""

    # Cabeçalho
    output_string += Fore.BLUE + Style.BRIGHT + "Cálculo da Glosa de Jitter" + Style.RESET_ALL + "\n"

    # Fórmula
    output_string += Fore.YELLOW + "Fórmula:" + Style.RESET_ALL + "\n"
    output_string += Fore.MAGENTA + "G = ((Jm - Jl)/1) * d * C" + Style.RESET_ALL + "\n"

    # Tabela de variáveis (inicialmente vazia)
    tabela = PrettyTable()
    tabela.field_names = ["Variável", "Valor"]

    # Inicializar 'discount' com um valor padrão
    discount = 0  

    # Definir os descontos baseados na incidência
    if incidence == 2:
        if jitter <= 100 and jitter > quality_threshold:
            discount = 0.0005 * latency_occurrences_percentile_95
        elif jitter > 100:
            discount = 0.005 * latency_occurrences_percentile_95
    elif incidence == 3:
        if jitter <= 100 and jitter > quality_threshold:
            discount = 0.001 * latency_occurrences_percentile_95
        elif jitter > 100:
            discount = 0.01 * latency_occurrences_percentile_95
    elif incidence == 4:
        if jitter <= 100 and jitter > quality_threshold:
            discount = 0.002 * latency_occurrences_percentile_95
        elif jitter > 100:
            discount = 0.02 * latency_occurrences_percentile_95
    else:
        discount = 0  # Sem desconto para outras incidências

    # Calcular a glosa considerando o número de ocorrências
    gloss = ((jitter - quality_threshold) / 1) * discount * value_month

    # Popular a tabela com os valores
    tabela.add_row(["P95{Ln}m", f"{jitter} ms"])
    tabela.add_row(["P95{Ln}i", f"{quality_threshold} ms"])
    tabela.add_row(["d", discount])
    tabela.add_row(["C", f"R$ {value_month}"])

    # Adicionar a tabela à string de saída
    output_string += str(tabela) + "\n"
    output_string += Fore.YELLOW + "Resultado:" + Style.RESET_ALL + "\n"
    # Cálculo da glosa
    output_string += Fore.GREEN + f"G = {locale.currency(gloss, grouping=True, symbol=False)}" + Style.RESET_ALL

    return output_string, gloss