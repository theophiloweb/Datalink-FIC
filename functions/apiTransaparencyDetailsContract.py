import os
import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()  # Iniciar DotEnv

def api_transparencia_details(id):
    # Verifica se é um CNPJ válido
    proxies = {
        'http': os.getenv("HTTP"),
        'https': os.getenv("HTTPS")
    }

    pag = 1
    url = f"{os.getenv('URL_TRANSPARENCIA')}/contratos/itens-contratados"
    params_url = {"id": id, "pagina": pag}
    headers_url = {os.getenv('KEY_TRANSPARENCIA'): os.getenv("VALUE_TRANSPARENCIA")}
    contract_details = []

    with tqdm(desc="Buscando dados detalhados", unit=" página") as pbar:
        while True:
            try:
                response = requests.get(url, params=params_url, headers=headers_url, proxies=proxies)
                response.raise_for_status()  # Levanta uma exceção para respostas de erro HTTP
            except requests.exceptions.HTTPError as http_err:
                print(f"Erro HTTP: {http_err}")
                break
            except requests.exceptions.ConnectionError as conn_err:
                print(f"Erro de Conexão: {conn_err}")
                break
            except requests.exceptions.Timeout as timeout_err:
                print(f"Timeout: {timeout_err}")
                break
            except requests.exceptions.RequestException as req_err:
                print(f"Erro de Requisição: {req_err}")
                break

            response_json = response.json()

            if not response_json:
                print("Nenhum dado encontrado ou fim dos dados.")
                pbar.close()
                break

            for item in response_json:
                   contract_details.append({
                      "numero": item["numero"], 
                      "descricao": item["descricao"],
                      "descComplementarItemCompra": item["descComplementarItemCompra"],
                      "monthly_payment": item["valor"],
                    })

            pag += 1
            params_url["pagina"] = pag
            pbar.update(1)

    return contract_details

