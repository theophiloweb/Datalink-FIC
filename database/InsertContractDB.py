import sqlite3
import hashlib
from colorama import init, Back, Fore, Style
from database.UserQueryDB import *

class InsertContractDB:
    def __init__(self, db_path, contract_data, contract_alias, id_company):
        self.db_path = db_path
        self.contract_data = dict(contract_data)
        self.contract_alias = contract_alias 
        self.id_company = id_company     
        self.msg = None
        self.cod = 160045
        
    def getMsg(self):
        return self.msg    

    def insert_contract(self):
        try:
            # Conectar ao banco de dados SQLite
            connection = sqlite3.connect(self.db_path)
            cursor = connection.cursor()   

           # Criar a tabela contract se ela ainda não existir
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS contract (
                    id INTEGER PRIMARY KEY,
                    company_id INTEGER,
                    contractor_id INTEGER,
                    contract_alias TEXT,       
                    number INTEGER,
                    object TEXT,
                    process_number TEXT,
                    signature_date DATE,
                    publication_date_DOU DATE,
                    initial_effective_date DATE,
                    final_effective_date DATE,
                    initial_value REAL,
                    final_value REAL,
                    FOREIGN KEY (company_id) REFERENCES company(id),
                    FOREIGN KEY (contractor_id) REFERENCES contractor(id)
                )
            """)   

            # Inserir os dados do contrato na tabela 'contract'
            # Pegar o ID da tabela contract
            cursor.execute("SELECT id FROM contractor WHERE cod = ?", (self.cod,))
            found = cursor.fetchone()
            cursor.execute("""
                    INSERT INTO contract (id, company_id, contractor_id, contract_alias, number, object, process_number, signature_date, publication_date_DOU, initial_effective_date, final_effective_date, initial_value, final_value)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    self.contract_data["id"],
                    self.id_company,
                    found[0],
                    self.contract_alias,
                    self.contract_data["number"],
                    self.contract_data["object"],
                    self.contract_data["process_number"],
                    self.contract_data["signature_date"],
                    self.contract_data["publication_date_DOU"],
                    self.contract_data["initial_effective_date"],
                    self.contract_data["final_effective_date"],
                    self.contract_data["initial_value"],
                    self.contract_data["final_value"]
                ))

            # Commit da transação e fechamento da conexão
            connection.commit()
            connection.close()

            self.msg =  f"{Fore.BLUE}Contrato inserido com sucesso no banco de dados..{Fore.RESET}"             

        except Exception as e:
            self.msg = f"{Fore.BLUE}Error: Falha ao inserir o Contrato no banco de dados: {e}.{Fore.RESET}" 
            

