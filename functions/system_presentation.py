import textwrap
import shutil
import os
from art import text2art
from colorama import Fore

def system_presentation():
    # Texto a ser convertido em arte ASCII
    text = "DarkSystem"
    green_color = Fore.GREEN  # Verde
    blue_color = Fore.BLUE    # Azul
    reset_color = Fore.RESET  # Reseta a cor

    # Convertendo o texto em arte ASCII
    artwork = text2art(text, font="rnd-medium")

    # Obtém as dimensões do terminal
    terminal_columns, _ = shutil.get_terminal_size()

    # Centraliza a arte ASCII
    centralized_art = '\n'.join(['{:^{}}'.format(linha, terminal_columns) for linha in artwork.split('\n')])

    # Imprime a arte ASCII centralizada com gradiente de cores
    for i, linha in enumerate(centralized_art.split('\n')):
        # Calcula a cor intermediária com base na posição na linha
        interpolation_ratio = i / (len(centralized_art.split('\n')) - 1)
        interpolated_color = Fore.LIGHTGREEN_EX if interpolation_ratio < 0.5 else Fore.LIGHTBLUE_EX

        # Imprime a linha com a cor intermediária
        print(f"{interpolated_color}{linha}{reset_color}")

    # Texto de título e informações adicionais
    title = (
        f"{Fore.MAGENTA}DataLink - Operações relacionadas a enlaces e conectividade {Fore.RESET}\n"
        f"{Fore.MAGENTA}© Copyright 2024 DarkSystem Automação e desenvolvimento {Fore.RESET}\n"
        f"{Fore.BLUE}Desenvolvido pelo ST Teófilo{Fore.RESET}\n"
    )

    # Centralizando o título do sistema   
    print(textwrap.indent(title, ' ' * 43))

