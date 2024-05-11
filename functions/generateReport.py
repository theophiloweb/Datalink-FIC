from docx import Document
from datetime import datetime
import os
import sys
import re
import string

def write_report_data(
                    numero_contrato,dateStart,objeto,contratante,fornecedor,cnpj,Dl,disp_coletada,perda_pacotes_coleta,latencia_coletada,      jitter_coletado,disp_empresa,perda_pacotes_empresa,latencia_empresa,jitter_empresa,incidence,incidence_pct_loss,incidence_latency,incidence_jitter,gloss_availability_numeric,gloss_pct_numeric,gloss_latency_numeric,gloss_jitter_numeric,valor_contrato,gloss_availability,gloss_latency,gloss_jitter,gloss_pct,fiscal,cargo
                    ):

    # diretório atual
    current_dir = os.path.dirname(__file__)

    # Subir um nível
    parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

    #caminho para o arquivo docx
    template_path = os.path.join(parent_dir, 'data', 'relatorio.docx')

    # Criar um novo documento com base no modelo
    doc_copy = Document(template_path)

    data_obj = datetime.strptime(dateStart, "%d-%m-%Y %H:%M:%S")  # Formato com horário
    month = data_obj.strftime("%B")  # Extrair o mês por extenso
    year = data_obj.strftime("%Y")  # Extrair o ano no formato AAAA
    formatted_date = data_obj.strftime("%d de %B de %Y")  # Formatar a data

   
    # Verificar se o arquivo existe
    if os.path.exists(template_path):
        # Carregar o documento
        doc = doc_copy

        # Iterar sobre as tabelas do documento
        for table in doc.tables:
            # Iterar sobre as linhas da tabela
            for row in table.rows:
                # Iterar sobre as células da linha
                for cell in row.cells:
                    original_text = cell.text
                    # Substituir as marcações pelos valores correspondentes
                    cell.text = str(cell.text.replace('{numero_contrato}', numero_contrato))
                    cell.text = str(cell.text.replace('{mes}',month))
                    cell.text = str(cell.text.replace('{ano}',year))
                    cell.text = str(cell.text.replace('{objeto}', objeto))
                    cell.text = str(cell.text.replace('{contratante}', contratante))
                    cell.text = str(cell.text.replace('{fornecedor}', fornecedor))
                    cell.text = str(cell.text.replace('{cnpj}', cnpj))
                    cell.text = str(cell.text.replace('{Dl}', str(Dl)))
                    cell.text = str(cell.text.replace('{disp_coletada}', str(disp_coletada)))
                    cell.text = str(cell.text.replace('{perda_pacotes_coleta}', str(perda_pacotes_coleta)))
                    cell.text = str(cell.text.replace('{latencia_coletada}', f"{latencia_coletada} ms"))
                    cell.text = str(cell.text.replace('{jitter_coletado}', f"{jitter_coletado} ms"))                  
                    cell.text = str(cell.text.replace('{disp_empresa}', f"{disp_empresa}%"))
                    cell.text = str(cell.text.replace('{perda_pacotes_empresa}', f"{perda_pacotes_empresa}ms"))
                    cell.text = str(cell.text.replace('{latencia_empresa}', f"{latencia_empresa}ms"))
                    cell.text = str(cell.text.replace('{jitter_empresa}', f"{jitter_empresa}ms"))
                    if int(incidence) == 1:
                        cell.text = str(cell.text.replace('{disp_1}', 'x'))
                    elif int(incidence) == 2:
                        cell.text = str(cell.text.replace('{disp_2}', 'x'))
                    elif int(incidence) == 3:
                        cell.text = str(cell.text.replace('{disp_3}', 'x'))
                    else:
                        cell.text = str(cell.text.replace('{disp_SI}', 'x'))

                    if int(incidence_pct_loss) == 1:
                        cell.text = str(cell.text.replace('{pct_1}', 'x'))
                    elif int(incidence_pct_loss) == 2:
                        cell.text = str(cell.text.replace('{pct_2}', 'x'))
                    elif int(incidence_pct_loss) == 3:
                        cell.text = str(cell.text.replace('{pct_3}', 'x'))
                    elif int(incidence_pct_loss) == 4:
                         cell.text = str(cell.text.replace('{pct_4}', 'x'))    
                    else:
                        cell.text = str(cell.text.replace('{pct_SI}', 'x'))  

                    if int(incidence_latency) == 1:
                        cell.text = str(cell.text.replace('{lat_1}', 'x'))
                    elif int(incidence_latency) == 2:
                        cell.text = str(cell.text.replace('{lat_2}', 'x'))
                    elif int(incidence_latency) == 3:
                        cell.text = str(cell.text.replace('{lat_3}', 'x'))
                    elif int(incidence_latency) == 4:
                         cell.text = str(cell.text.replace('{lat_4}', 'x'))    
                    else:
                        cell.text = str(cell.text.replace('{lat_SI}', 'x'))  

                    if int(incidence_jitter) == 1:
                        cell.text = str(cell.text.replace('{jit_1}', 'x'))
                    elif int(incidence_jitter) == 2:
                        cell.text = str(cell.text.replace('{jit_2}', 'x'))
                    elif int(incidence_jitter) == 3:
                        cell.text = str(cell.text.replace('{jit_3}', 'x'))
                    elif int(incidence_jitter) == 4:
                         cell.text = str(cell.text.replace('{jit_4}', 'x'))    
                    else:
                        cell.text = str(cell.text.replace('{jit_SI}', 'x'))   
                                      
                    cell.text = str(cell.text.replace('{glosa_disp}', str(gloss_availability_numeric)))
                    cell.text = str(cell.text.replace('{glosa_pct}', str(gloss_pct_numeric)))
                    cell.text = str(cell.text.replace('{glosa_lat}', str(gloss_latency_numeric)))
                    cell.text = str(cell.text.replace('{glosa_jit}', str(gloss_jitter_numeric)))
                    cell.text = str(cell.text.replace('{valor_contrato}', str(valor_contrato)))
                    sum = round((gloss_availability_numeric + gloss_pct_numeric + gloss_latency_numeric + gloss_jitter_numeric),2)
                    cell.text = str(cell.text.replace('{valor_total_glosa}', str(sum)))
                    if sum > valor_contrato:
                       cell.text = str(cell.text.replace('{valor_na_nota}', str(0)))
                    else:
                       cell.text = str(cell.text.replace('{valor_na_nota}', str(float({valor_contrato - sum}))))     

                    if int(incidence) > 0 and gloss_availability is not None:
                       cleaned_gloss_availability = ''.join(filter(lambda x: x in string.printable, gloss_availability)) 
                       cell.text = str(cell.text.replace('{calc_glosa_disp}', str(cleaned_gloss_availability)))
                    else:
                       cell.text = str(cell.text.replace('{calc_glosa_disp}', f"Sem glosa"))  

                    if int(incidence_latency) > 0 and gloss_latency is not None:
                       cleaned_gloss_latency = ''.join(filter(lambda x: x in string.printable, gloss_latency))  
                       cell.text = str(cell.text.replace('{calc_glosa_lat}', str(cleaned_gloss_latency)))
                    else:
                       cell.text = str(cell.text.replace('{calc_glosa_lat}',"Sem glosa"))

                    if int(incidence_jitter) > 0 and gloss_jitter is not None:
                       cleaned_gloss_jitter = ''.join(filter(lambda x: x in string.printable, gloss_jitter))   
                       cell.text = str(cell.text.replace('{calc_glosa_jit}', str(cleaned_gloss_jitter)))
                    else:
                       cell.text = str(cell.text.replace('{calc_glosa_jit}', "Sem glosa"))

                    if int(incidence_pct_loss) > 0 and gloss_pct is not None:
                       cleaned_gloss_pct = ''.join(filter(lambda x: x in string.printable, gloss_pct))    
                       cell.text = str(cell.text.replace('{calc_glosa_pct}', str(cleaned_gloss_pct)))
                    else:
                       cell.text = str(cell.text.replace('{calc_glosa_pct}',"Sem glosa"))  

                    cell.text = str(cell.text.replace('{data_rodapé}', str(formatted_date)))
                    cell.text = str(cell.text.replace('{fiscal}', str(fiscal)))
                    cell.text = str(cell.text.replace('{cargo}', str(cargo)))                  



        # Salvar as alterações no documento
        name_doc = f"relatorio_{numero_contrato}_{dateStart}.docx"
        report_path = os.path.join(parent_dir, 'data', name_doc)
        doc.save(report_path)

        # Exibir a mensagem de sucesso
        print("Relatório gerado com sucesso.")
    else:
        print("O arquivo relatorio.docx não foi encontrado.")

