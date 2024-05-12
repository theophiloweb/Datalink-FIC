# Darklink FIC - Fiscalização Inteligente de Contratos

[![Python](https://img.shields.io/badge/Python-3.7%2B-blue.svg)](https://www.python.org/)
[![Zabbix API](https://img.shields.io/badge/Zabbix%20API-v5.4-green.svg)](https://www.zabbix.com/documentation/current/en/manual/api)
[![Gemini API](https://img.shields.io/badge/Gemini%20API-v1.5-brightgreen.svg)](https://developers.generativeai.google/)
[![SQLite](https://img.shields.io/badge/SQLite-3-orange.svg)](https://www.sqlite.org/index.html)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

![Darklink FIC Banner](./images/linkops.ico) 

O Darklink FIC é um sistema de automação em Python que utiliza inteligência artificial para fiscalizar o desempenho de contratos de serviços de rede. A solução integra dados do Zabbix, API de Transparência e Google Gemini para gerar relatórios detalhados com análises e possíveis sanções. 

# Simulação da Análise com IA

Para fins de demonstração e validação do sistema, a análise com Inteligência Artificial (IA), que normalmente ocorreria ao final do processo de coleta de dados, foi simulada nesta versão.

Em vez de executar todo o processo de coleta de dados (requerendo acesso à API do Zabbix, API da Transparência, bibliotecas do Python, etc.), o texto a ser analisado pela IA foi definido diretamente no início do arquivo `Main.py`, juntamente com a criação de variáveis com valores fictícios.

Essa abordagem permite verificar a funcionalidade da IA e a geração da análise sem a necessidade de percorrer todo o fluxo do sistema. É importante destacar que essa é uma solução temporária para fins didáticos e de desenvolvimento.

Em um ambiente de produção, o sistema completo seria executado, incluindo a coleta de dados reais e a análise final pela IA.


## Funcionalidades

* **Coleta automatizada de indicadores de rede:** Latência, Jitter, Perda de Pacotes e Disponibilidade via Zabbix API.
* **Comparação com indicadores do provedor:** Validação da conformidade com os termos do contrato.
* **Geração de relatórios personalizados:** Análise completa, incluindo potenciais sanções com base em regras configuráveis.
* **Integração com API de Transparência:** Enriquecimento dos relatórios com dados públicos.
* **Análise com IA (Google Gemini):** Interpretação de dados, identificação de padrões e sugestões de ações corretivas.

## Requisitos

* Python 3.7+
* Bibliotecas Python: `zabbix-api`, `requests`, `sqlite3`, `colorama`, `google-generativeai`, `python-dotenv`, `textwrap`, `json`, `docx`, `string`, `prettytable`, `locale`, `os`, `re`, `dotenv`, `art`, `sys`, `dateutil`, `getpass`, `time`, `tqdm`, etc.
* Arquivo `.env` com:
    * Credenciais da API Zabbix
    * Token da API de Transparência
    * Token da API Google Gemini 
    * HostIDs do Zabbix para itens contratuais
    * Caminho para o banco de dados SQLite3 
* Triggers configuradas no Zabbix para os itens relevantes.
* Modelos de relatório personalizados.

## Utilização

1. Instale as bibliotecas necessárias.
2. Configure o arquivo `.env` com as informações relevantes.
3. Execute o sistema via terminal.
4. Siga as instruções para selecionar o contrato e gerar o relatório.

## Classe Item.py

A classe `Item.py` é crucial para a interação com o Zabbix. Ela exibe os itens dos hosts especificados no arquivo `.env`. É fundamental que os desenvolvedores compreendam o funcionamento dessa classe e a configurem para o ambiente específico, ajustando os parâmetros e métodos conforme necessário.

## Personalização

* **Modelos de Relatório:** Adapte os modelos de relatório (`generateReport.py`) para as necessidades específicas da sua organização.
* **Regras de Sanção:** Configure as regras de aplicação de sanções com base nos termos dos seus contratos.
* **Triggers do Zabbix:** Assegure que as triggers no Zabbix estejam configuradas corretamente para disparar alertas e coletar os dados relevantes.

## Vídeo de apresentação e uso do Sistema
Youtube - [Teophilo Silva](https://www.youtube.com/watch?v=RCdPwnyE4WA) 

## Próximos Passos

* Implementar interface gráfica para facilitar a utilização.
* Integrar com outras plataformas de monitoramento de rede.
* Expandir a análise com IA para identificar padrões complexos e prever problemas de desempenho.

## Contribuições

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues e enviar pull requests.

## Licença

Este projeto está licenciado sob a licença MIT. 

## Contato

Linkedin - [Teophilo Silva](www.linkedin.com/in/teophilo-silva-dev) 

---

**Observações:**

* Substitua `./images/img.png` pelo caminho da imagem real do banner.
* Adapte o texto com as informações específicas do seu projeto.
