# (Imports que você já tem no seu arquivo)
from cadastro import carregar_usuarios, carregar_pontos, salvar_usuarios, salvar_pontos
from utils import limpar_tela, aguardar, validar_senha, validar_email
import json
from rich.console import Console
from rich.prompt import Prompt
from rich.panel import Panel

console = Console()

def login():
    limpar_tela()
    console.rule("[bold cyan]--- 🔒 TELA DE LOGIN ---[/bold cyan]")

    console.print("1. Logar", style="bold green")
    console.print("2. Esqueci minha senha", style="bold yellow")
    console.print("0. Voltar ao menu principal", style="bold red")
    opcao_login = Prompt.ask("\n[bold cyan]Escolha uma opção[/bold cyan]")

    if opcao_login == '1':
        pass
    elif opcao_login == '2':
        esqueci_minha_senha()
        return login()  
    elif opcao_login == '0':
        return 
    else:
        console.print("\n[bold red]❌ Opção inválida![/bold red]")
        aguardar(1)

    while True:
        email_login = Prompt.ask("\n[bold]Digite seu email[/bold]")

        conta_encontrada = None
        tipo_conta = None 

        usuarios = carregar_usuarios()
        for usuario in usuarios:
            if usuario['email'] == email_login:
                conta_encontrada = usuario 
                tipo_conta = "usuario"
                break 

        if not conta_encontrada:
            pontos = carregar_pontos()
            for ponto in pontos:
                if ponto['email'] == email_login:
                    conta_encontrada = ponto 
                    tipo_conta = "ponto"
                    break
        
        if not conta_encontrada:
            console.print("\n[bold red]❌ Email não cadastrado no sistema. Tente novamente.[/bold red]")
            aguardar(2)
            limpar_tela()
            console.rule("[bold cyan]--- 🔒 TELA DE LOGIN ---[/bold cyan]")
            continue

        console.print(f"[bold green]Email encontrado![/bold green] Agora digite a senha.")
      
        while True:
            senha_login = Prompt.ask("\nDigite sua senha", password=True)

            if conta_encontrada['senha'] == senha_login:
                if tipo_conta == "usuario":
                    aguardar(2)
                    return "usuario", usuario

                elif tipo_conta == "ponto":
                    aguardar(2)
                    return "ponto", ponto
            
            else:
                console.print("\n[bold red]❌ Senha incorreta[/bold red]")
                confirmar = Prompt.ask("[bold yellow]Deseja redefinir a senha?[/bold yellow]", choices=["1", "2"])
                if confirmar == '1':
                    esqueci_minha_senha()
                    return login()  
                else:
                    console.print("Digite a senha novamente.", style="italic cyan")
                aguardar(1)

def esqueci_minha_senha():
    limpar_tela()
    console.rule("[bold yellow]--- 🔑 RECUPERAÇÃO DE SENHA ---[/bold yellow]")
    email_rec = Prompt.ask("Digite o email da conta que você quer recuperar")

    if not validar_email(email_rec):
        console.print("\n[bold red]❌ Formato de email inválido. Tente novamente.[/bold red]")
        aguardar(2)
        return

    usuarios = carregar_usuarios()
    for i, usuario in enumerate(usuarios):
        if usuario['email'] == email_rec:
            console.print(f"\n[bold green]Encontramos a conta de usuário:[/bold green] {usuario.get('nome', 'Usuário')}")
            nova_senha = pedir_nova_senha_validada() 
            if nova_senha:
                usuarios[i]['senha'] = nova_senha
                salvar_usuarios(usuarios) 
                console.print("\n✅ [bold green]Senha de USUÁRIO alterada com sucesso![/bold green]")
                aguardar(2)
                return 

    pontos = carregar_pontos()
    for i, ponto in enumerate(pontos):
        if ponto['email'] == email_rec:
            console.print(f"\n[bold green]Encontramos a conta de ponto de coleta:[/bold green] {ponto.get('nome_ponto', 'Ponto')}")
            nova_senha = pedir_nova_senha_validada()
            if nova_senha:
                pontos[i]['senha'] = nova_senha
                salvar_pontos(pontos) 
                console.print("\n✅ [bold green]Senha de PONTO DE COLETA alterada com sucesso![/bold green]")
                aguardar(2)
                return

    console.print("\n[bold red]❌ Email não encontrado em nosso sistema.[/bold red]")
    aguardar(3)

def pedir_nova_senha_validada():
    while True:
        nova_senha = Prompt.ask("Digite sua nova senha", password=True)
        resultado_nova_senha = validar_senha(nova_senha)
        if resultado_nova_senha == "Aprovada!":
            confirmar_senha = Prompt.ask("Confirme sua nova senha", password=True)
            if nova_senha == confirmar_senha:
                return nova_senha 
            else:
                console.print("\n    ❌ [bold red]As senhas não coincidem. Tente novamente.[/bold red]")
                
        elif resultado_nova_senha == "A senha não contém letra":
            console.print("[bold yellow]A senha não contém letra[/bold yellow]")
        elif resultado_nova_senha == "A senha não contém número":
            console.print("[bold yellow]A senha não contém número[/bold yellow]")
        elif resultado_nova_senha == "A senha deve haver no mínimo 8 caracteres.":
            console.print("[bold yellow]A senha deve haver no mínimo 8 caracteres.[/bold yellow]")
        elif resultado_nova_senha == "A senha não pode conter caracteres especiais.":
            console.print("[bold yellow]A senha não pode conter caracteres especiais.[/bold yellow]")
        else:
            console.print("[bold red]Tente novamente[/bold red]")


