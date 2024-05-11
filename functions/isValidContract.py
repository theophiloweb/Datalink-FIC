import re
from colorama import Fore, Style

# Função para validar o número do contrato
def isValidContract():
    while True:
        contract = input("Digite o número do contrato (formato: 10/2021): ")
        if re.match(r'^\d{1,2}/\d{4}$', contract):
            print(Fore.GREEN + "Número do contrato é válido." + Style.RESET_ALL)
            return contract
        else:
            print(Fore.RED + "Número do contrato inválido. Tente novamente." + Style.RESET_ALL)


