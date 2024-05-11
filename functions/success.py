import os
from art import *
import textwrap
from colorama import Fore


def sucess():

    success_text = "OK"   
    success_art = text2art(success_text, font="small")
    centralized_art = textwrap.indent(success_art, ' ' * 43)  
    print(f"{Fore.GREEN}{centralized_art}{Fore.RESET}")