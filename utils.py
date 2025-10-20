import os
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()
aguardar = time.sleep

def limpar_tela():
    """Limpa o terminal, com título visual opcional."""
    if os.name == 'nt': 
        os.system('cls')
    else:  
        os.system('clear')


def validar_senha(teste):
    """Valida uma senha e retorna mensagens visuais com Rich."""
    if len(teste) < 8:
        console.print(Panel("[bold red]❌ A senha deve conter no mínimo 8 caracteres.[/bold red]", box=box.ROUNDED))
        return "A senha deve haver no mínimo 8 caracteres."
    
    letra = False
    numero = False

    for caractere in teste:
        if caractere.isalpha():
            letra = True
        elif caractere.isdigit():
            numero = True
        else:
            console.print(Panel("[bold red]❌ A senha não pode conter caracteres especiais.[/bold red]", box=box.ROUNDED))
            return "A senha não pode conter caracteres especiais."

    if not letra:
        console.print(Panel("[bold yellow]⚠️ A senha deve conter pelo menos uma letra.[/bold yellow]", box=box.ROUNDED))
        return "A senha não contém letra"
    
    if not numero:
        console.print(Panel("[bold yellow]⚠️ A senha deve conter pelo menos um número.[/bold yellow]", box=box.ROUNDED))
        return "A senha não contém número"

    console.print("[green]✔ Senha válida![/green]")
    return "Aprovada!"


def validar_email(email):
    """Valida um email e retorna True ou False."""
    posicao_arroba = email.find("@")
    posicao_ponto = email.rfind(".")
    
    if posicao_arroba > 0 and posicao_ponto > posicao_arroba + 1 and not email.endswith("."):
        if email.count("@") == 1:
            return True

    console.print(Panel("[bold red]❌ Email inválido![/bold red] Tente novamente.", box=box.ROUNDED))
    return False
