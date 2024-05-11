from colorama import Fore, Style  # Cores e estilos
from prettytable import PrettyTable
import locale

def gloss_availability(index_contract, percentage_availability, valor_final_compra, incidence):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    index_contract = float(index_contract)  # Ensure numerical type (if needed)
    percentage_availability = float(percentage_availability)  # Ensure numerical type (if needed)
    if percentage_availability >= index_contract:
        print("Parabéns, sem glosa para o período.")
        return 

    # Cálculo da diferença entre o limiar de qualidade (Dl) e a disponibilidade medida (Dm)
    difference = index_contract - percentage_availability

    if incidence == 2:
        # Verificar se a disponibilidade medida é menor que o limiar de qualidade
        if percentage_availability < index_contract:
            # Calcular o desconto (d) com base na diferença
            if percentage_availability < 95:
                d = round((difference/0.1) * 1, 2)  # Se Dm < 95, d = 30 * 1%
            else:
                d = round((difference/0.1) * 0.5, 2)  # Se Dm > 95, d = (Dl - Dm) * 10 * 0.5%
        else:
            d = 0  # Se Dm >= Dl, não há desconto
    else:
        # Verificar se a disponibilidade medida é menor que o limiar de qualidade
        if percentage_availability < index_contract:
            # Calcular o desconto (d) com base na diferença
            if percentage_availability < 95:
                d = round((difference/0.1) * 2, 2)  # Se Dm < 95, d = 30 * 1%
            else:
                d = round((difference/0.1) * 1, 2)  # Se Dm > 95, d = (Dl - Dm) * 10 * 0.5%
        else:
            d = 0  # Se Dm >= Dl, não há desconto

    # Cálculo da glosa (G)
    gloss_pure = round((((index_contract/100) - (percentage_availability/100)) / 0.001) * d * valor_final_compra, 2)    
    gloss_formated = locale.currency(gloss_pure, grouping=True, symbol=False)

    # Construção da string com os prints
    output_string = ""  # Inicializa a string vazia

    # Cabeçalho
    output_string += Fore.BLUE + Style.BRIGHT + "Fórmula de Cálculo da Glosa da Indisponibilidade" + Style.RESET_ALL + "\n"
    output_string += Fore.MAGENTA + f"G = (((Dl/100) - (Dm/100)) / 0.001) * d * C" + Style.RESET_ALL + "\n"
    
    # Tabela de variáveis
    tabela = PrettyTable()
    tabela.add_column("Variável", ["Dl", "Dm", "d", "C"])
    tabela.add_column("Valor", [f"{index_contract}%", f"{percentage_availability}%", d, f"R$ {valor_final_compra}"])
    output_string += str(tabela) + "\n"  # Adiciona a tabela à string

    # Fórmula
    output_string += Fore.YELLOW + "Resultado:" + Style.RESET_ALL + "\n"

    # Cálculo da glosa
    output_string += Fore.GREEN + f"G = {gloss_formated}" + Style.RESET_ALL 

    return output_string, gloss_pure  # Retorna a string completa com os prints


