from utils import limpar_tela
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.prompt import IntPrompt

console = Console()

def menu_inicial():
    limpar_tela()
    console.rule("[bold bright_green]🌿 MENU INICIAL 🌿", style="green")
    
    console.print("\n[bold cyan]1[/] - Tutorial")
    console.print("[bold cyan]2[/] - Cadastro")
    console.print("[bold cyan]3[/] - Login")
    console.print("[bold red]0[/] - Fechar Menu\n")
    
    try:
        entrada = IntPrompt.ask("[bold yellow]Qual função deseja?[/]")
        return entrada
    except ValueError:
        return -1


def menu_ponto(usuario_logado):
    limpar_tela()
    titulo = Text("🏢 PAINEL DO PONTO", style="bold blue")
    subtitulo = f"Bem-vindo(a), [bold green]{usuario_logado['nome_ponto']}[/bold green]!"
    console.print(Panel.fit(subtitulo, title=titulo, border_style="bright_blue"))
    
    console.print("\n[bold cyan]1.[/] Cadastrar reciclagem")
    console.print("[bold cyan]2.[/] Impactos")
    console.print("[bold cyan]3.[/] Perfil")
    console.print("[bold red]0.[/] Sair\n")
    
    try:
        entrada_usuario = IntPrompt.ask("[bold yellow]Escolha uma opção[/]",)
        return entrada_usuario
    except ValueError:
        return -1


def menu_usuario(usuario_logado):
    limpar_tela()
    titulo = Text("👤 PAINEL DO USUÁRIO", style="bold magenta")
    subtitulo = f"Bem-vindo(a), [bold green]{usuario_logado['nome']}[/bold green]!"
    console.print(Panel.fit(subtitulo, title=titulo, border_style="bright_magenta"))
    
    console.print("\n[bold cyan][1][/bold cyan] Encontrar pontos de coleta")
    console.print("[bold cyan][2][/bold cyan] Calcular pontuação")
    console.print("[bold cyan][3][/bold cyan] Impactos")
    console.print("[bold cyan][4][/bold cyan] Indicações")
    console.print("[bold cyan][5][/bold cyan] Tutorial")
    console.print("[bold cyan][6][/bold cyan] Meu perfil")
    console.print("[bold red][0][/bold red] Sair da conta\n")
    
    try:
        entrada_usuario = IntPrompt.ask("[bold yellow]Escolha uma opção[/]",)
        return entrada_usuario
    except ValueError:
        return -1
