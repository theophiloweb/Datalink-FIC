from colorama import Fore, Style

def provider_indicators():
    """
    Solicita ao usuário os indicadores do provedor (latência, jitter, perda de pacotes, disponibilidade) 
    e retorna uma lista com os valores em formato float.
    """

    while True:
        user_input = input(
            f"{Fore.CYAN}Por favor, insira os indicadores do provedor separados por espaço (latência jitter perda_pacotes disponibilidade):{Style.RESET_ALL} \n "
        )
        try:
            # Tenta converter a entrada do usuário em uma lista de floats
            indicators = [float(x) for x in user_input.split()]

            # Verifica se foram inseridos exatamente 4 valores
            if len(indicators) != 4:
                raise ValueError("Você deve inserir exatamente 4 valores.")

            # Apresenta os dados inseridos e confirma com o usuário
            print(f"{Fore.YELLOW}Você inseriu os seguintes valores:")
            print(f"Latência: {indicators[0]} ms")
            print(f"Jitter: {indicators[1]} ms")
            print(f"Perda de Pacotes: {indicators[2]}%")
            print(f"Disponibilidade: {indicators[3]}%{Style.RESET_ALL}")

            confirm = input("Os dados estão corretos? (s/n): ")
            if confirm.lower() == 's':
                return indicators

        except ValueError:
            print(f"{Fore.RED}Entrada inválida. Por favor, insira 4 valores numéricos separados por espaço.{Style.RESET_ALL}")