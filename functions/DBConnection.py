import sys
from colorama import init, Back, Fore, Style
from database.Database import *
from dotenv import load_dotenv
import os


def DBConnection():

    #CONEXÃO COM DATABASE E RETORNOS  
        load_dotenv()
        db_path = os.getenv("DB_PATH")        
        db = Database(db_path)
        response = db.connect()          
        if response == 1:
          print(f"{Fore.RED}Arquivo do banco de dados não encontrado.{Fore.RESET}")
          sys.exit(1)  # Sai com código de erro 1

        elif response == 2:
          print(f"{Fore.GREEN}Tabela 'user' e 'contractor' criadas com sucesso.{Fore.RESET}")

        elif response == 3:
          print(f"{Fore.GREEN}Conexão estabelecida com sucesso.{Fore.RESET}")
          print(db.close())