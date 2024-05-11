import re

def isValidPhone(phone):
    standard_phone = r'^\(?(\d{2})\)?[\s-]?(\d{4,5})-?(\d{4})$'
    while not re.match(standard_phone, phone):
        phone = input("Número inválido. Por favor, insira um número de telefone válido: ")
    return phone
