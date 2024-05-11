import os
import requests
from dotenv import load_dotenv
from tqdm import tqdm

load_dotenv()  # Iniciar DotEnv

def api_transparencia_request(cnpj):
    # Verifica se é um CNPJ válido
    proxies = {
        'http': os.getenv("HTTP"),
        'https': os.getenv("HTTPS")
    }

    pag = 1
    url_base = f"{os.getenv('URL_TRANSPARENCIA')}/contratos/cpf-cnpj"
    params = {"cpfCnpj": cnpj, "pagina": pag}
    headers = {os.getenv('KEY_TRANSPARENCIA'): os.getenv("VALUE_TRANSPARENCIA")}
    selected_keys = []

    with tqdm(desc="Buscando dados", unit=" página") as pbar:
        while True:
            try:
                response = requests.get(url_base, params=params, headers=headers, proxies=proxies)
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
                if item["unidadeGestora"]["codigo"] == '160045':
                    selected_keys.append({
                        "id": item["id"],
                        "numero": item["numero"],
                        "objeto": item["objeto"],
                        "compra_numero": item["compra"]["numero"],
                        "compra_objeto": item["compra"]["objeto"],
                        "compra_numeroProcesso": item["compra"]["numeroProcesso"],
                        "unidadeGestora_codigo": item["unidadeGestora"]["codigo"],
                        "unidadeGestora_nome": item["unidadeGestora"]["nome"],
                        "dataAssinatura": item["dataAssinatura"],
                        "dataPublicacaoDOU": item["dataPublicacaoDOU"],
                        "dataInicioVigencia": item["dataInicioVigencia"],
                        "dataFimVigencia": item["dataFimVigencia"],
                        "fornecedor_cnpjFormatado": item["fornecedor"]["cnpjFormatado"],
                        "fornecedor_nome": item["fornecedor"]["nome"],
                        "valorInicialCompra": item["valorInicialCompra"],
                        "valorFinalCompra": item["valorFinalCompra"]
                    })

            pag += 1
            params["pagina"] = pag
            pbar.update(1)

    return selected_keys

