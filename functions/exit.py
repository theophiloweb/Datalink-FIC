import os
from art import *
import textwrap
from colorama import Fore


def exit():

    exit_text = "Saindo..."   
    exit_art = text2art(exit_text, font="small")
    centralized_art = textwrap.indent(exit_art, ' ' * 43)  
    print(f"{Fore.YELLOW}{centralized_art}{Fore.RESET}")