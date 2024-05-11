import re
from colorama import Fore, Style

# Instale o pacote colorama se ainda não estiver instalado:
# pip install colorama

def isValidCNPJ():

    def validates_cnpj(cnpj):
        # Remove caracteres indesejados
        cnpj = re.sub(r'[^0-9]', '', cnpj)

        # Verifica se o CNPJ tem 14 dígitos
        if len(cnpj) != 14:
            return False

        # Valida os dois dígitos verificadores
        soma = 0
        peso = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        for i in range(12):
            soma += int(cnpj[i]) * peso[i]

        resto = soma % 11
        if resto < 2:
            digito_verificador_1 = 0
        else:
            digito_verificador_1 = 11 - resto

        if int(cnpj[12]) != digito_verificador_1:
            return False

        soma = 0
        peso = [6, 5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
        for i in range(13):
            soma += int(cnpj[i]) * peso[i]

        resto = soma % 11
        if resto < 2:
            digito_verificador_2 = 0
        else:
            digito_verificador_2 = 11 - resto

        if int(cnpj[13]) != digito_verificador_2:
            return False

        return True

    while True:
        cnpj = input("Digite o CNPJ da Contratada: ")
        # Remover caracteres não numéricos
        cnpj = re.sub(r'[^0-9]', '', cnpj)
        if validates_cnpj(cnpj):
            print(Fore.GREEN + "CNPJ é válido." + Style.RESET_ALL)
            return cnpj
        else:
            print(Fore.RED + "CNPJ inválido. Tente novamente." + Style.RESET_ALL)

