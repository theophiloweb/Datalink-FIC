import re

def isValideEmail(email):
    standard_email = r'^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$'
    while not re.match(standard_email, email.lower()):
        email = input("Email inválido. Por favor, insira um email válido: ")
    return email
