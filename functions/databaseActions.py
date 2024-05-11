import os
import json
from colorama import *
from art import *
import textwrap

selected_contract = None

def database_actions(selected_keys,selected):

   
    global selected_contract

    #***********************************ADD CNPJ, CONTRACT, E ORGÃO PAGADOR*****************************************************
    # Exibindo o menu de seleção
    print("\033[1mSelecione um contrato pelo número:\033[0m")  # Título em negrito
    largura_maxima = max(len(item['numero'].lstrip('0')) for item in selected_keys)
    for i, item in enumerate(selected_keys, start=1):
        numero_contrato = item['numero'].lstrip('0')
        print(f"{str(i).rjust(2)}. {numero_contrato.ljust(largura_maxima)}")


    # Pedindo ao usuário para selecionar um contrato
    selected_index = int(input("Digite o número correspondente ao contrato desejado: ")) - 1

    # Verificando se o índice selecionado é válido
    if 0 <= selected_index < len(selected_keys):
        # Exibindo os detalhes do contrato selecionado
        selected_contract = selected_keys[selected_index]

        json_path = os.path.join('json', 'contract.json')  
        company_info = {}      
 
        for key, value in selected_contract.items():
                
                # Verificar se a chave está na lista de chaves desejadas
                if key in ['fornecedor_cnpjFormatado', 'fornecedor_nome', 'id', 'numero', 'unidadeGestora_codigo', 'unidadeGestora_nome', 'dataAssinatura', 'dataPublicacaoDOU', 'dataInicioVigencia', 'dataFimVigencia', 'valorInicialCompra', 'valorFinalCompra', 'descricao', 'descComplementarItemCompra', 'monthly_payment']:
                    # Adicionar a chave e o valor ao dicionário da empresa
                    company_info[key] = value

        # Salve as variáveis em um arquivo JSON
        with open(json_path, 'w') as f:
             json.dump(company_info, f)   

       

        selected_text = f"{selected_contract['numero']} = {selected}"   
        selected_art = text2art(selected_text, font='small')
        centralized_art = textwrap.indent(selected_art, ' ' * 20)  
        print(f"{Fore.BLUE}{centralized_art}{Fore.RESET}")        
        print("\n")   
        

        
    else:
        print("Índice selecionado inválido. Tente novamente.")
