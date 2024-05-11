import sys
import os
import getpass
from database.DBUserConnection import UserConnection


def login():

    login = input("Por favor digite seu CPF \n")
    password = getpass.getpass("Por favor digite sua senha \n")
    enter = UserConnection(login,password)
    enter.setPassword(password)
    response = enter.DBUserConnection()
    if response == False:
        sys.exit()
    os.system('cls' if os.name == 'nt' else 'clear')  
    return response    
