def select_option_index_availability():
    """
    Função para selecionar o índice de um contrato disponível.

    Retorna:
        int: O índice do contrato selecionado pelo usuário.
    """

    # Exibir opções para o usuário
    print('Agora vou pedir para você selecionar o índice de seu contrato para prosseguir...')
    print("Opções:")
    print("1 - 99")
    print("2 - 97")

    selected = int(input('Selecione o índice de seu contrato: '))

    while selected not in [1, 2]:  # Validação da entrada do usuário
        try:
            selected = int(input('Opção inválida. Selecione o índice de seu contrato: '))
            
        except ValueError:
            print("Valor inválido. Digite um número inteiro entre 1 e 2.")

    # Ajustar o índice selecionado conforme necessário
    if selected == 1:
        selected = 99
    elif selected == 2:
        selected = 97

    return selected


