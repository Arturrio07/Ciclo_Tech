from utils import limpar_tela, aguardar, validar_senha, validar_email
import requests
import json
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich import box

console = Console()

# =====================================================
#                  FUNÇÕES DE MENU
# =====================================================

def cadastro():
    limpar_tela()
    console.print(Panel.fit(
        "[bold cyan]📋 MENU DE CADASTRO[/bold cyan]\n\n"
        "[yellow]1[/yellow] - Cadastro de [green]Usuário[/green]\n"
        "[yellow]2[/yellow] - Cadastro de [magenta]Ponto[/magenta]\n"
        "[yellow]0[/yellow] - [red]Voltar ao menu[/red]",
        border_style="bright_blue"
    ))

    escolher_cadastro = int(Prompt.ask("[bold green]Escolha uma opção[/bold green]"))

    if escolher_cadastro == 1:
        cadastro_usuario()
    elif escolher_cadastro == 2:
        cadastro_ponto()
    elif escolher_cadastro == 0:
        console.print("[bold yellow]↩ Voltando ao menu...[/bold yellow]")
        aguardar(2)
        return 
    else:
        console.print("[bold red]❌ Insira um número válido![/bold red]")

# =====================================================
#                ENDEREÇO E ARQUIVOS
# =====================================================

def endereco():
    console.print(Panel.fit("[bold cyan]📍 ENDEREÇO DO PONTO[/bold cyan]", border_style="bright_cyan"))
    while True:
        cep = str(input("Cep: "))
        cep_limpo = "".join(filter(str.isdigit, cep))
        if len(cep_limpo) == 8:
            break
        else:
            console.print("[red]❌ Cep inválido, tente novamente.[/red]")

    rua = str(input("Rua: "))
    numero = str(input("Número da casa: "))
    bairro = str(input("Bairro: "))
    cidade = str(input("Cidade: "))
    estado = str(input("Estado: "))
    pais = str(input("País: "))

    endereco_formatado = {
        "cep": cep_limpo,
        "rua": rua,
        "numero": numero,
        "bairro": bairro,
        "cidade": cidade,
        "estado": estado,
        "pais": pais,
    }
    return endereco_formatado


def carregar_pontos():
    try:
        with open("pontos.json", "r", encoding="utf-8") as arquivo_ponto:
            conteudo_ponto = arquivo_ponto.read()
            if not conteudo_ponto:
                return []
            return json.loads(conteudo_ponto)
    except FileNotFoundError:
        with open("pontos.json", "w", encoding="utf-8") as arquivo_ponto:
            json.dump([], arquivo_ponto)
        return []


def salvar_pontos(lista_de_pontos):
    with open("pontos.json", "w", encoding="utf-8") as arquivo_ponto:
        json.dump(lista_de_pontos, arquivo_ponto, indent=4, ensure_ascii=False)


def carregar_usuarios():
    try:
        with open('usuarios.json', 'r', encoding="utf-8") as arquivo_usuario:
            conteudo_usuario = arquivo_usuario.read()
            if not conteudo_usuario:
                return []
            return json.loads(conteudo_usuario)
    except FileNotFoundError:
        with open("usuarios.json", "w", encoding="utf-8") as arquivo_usuario:
            json.dump([], arquivo_usuario)
        return []


def salvar_usuarios(lista_de_usuarios):
    with open('usuarios.json', 'w', encoding='utf-8') as arquivo_usuario:
        json.dump(lista_de_usuarios, arquivo_usuario, indent=4, ensure_ascii=False)

# =====================================================
#             FUNÇÕES DE VERIFICAÇÃO
# =====================================================

def email_existe(email_para_checar):
    usuarios = carregar_usuarios()
    pontos = carregar_pontos()

    for usuario in usuarios:
        if usuario['email'] == email_para_checar:
            return True 

    for ponto in pontos:
        if ponto['email'] == email_para_checar:
            return True 

    return False


def cpf_existe(cpf_checar):
    usuarios = carregar_usuarios()
    for usuario in usuarios:
        if usuario['cpf'] == cpf_checar:
            return True 
    return False


def cnpj_existe(cnpj_checar):
    pontos = carregar_pontos()
    for ponto in pontos:
        if ponto['cnpj'] == cnpj_checar:
            return True 
    return False


# =====================================================
#              CADASTRO DE PONTO
# =====================================================

def cadastro_ponto():
    limpar_tela()
    console.print(Panel.fit("[bold magenta]🏭 CADASTRO DE PONTO[/bold magenta]", border_style="bright_magenta"))

    while True:
        nome_ponto = str(input("Nome: "))
        if len(nome_ponto) < 5:
            console.print("[yellow]⚠ Digite um nome com no mínimo 5 caracteres.[/yellow]")
        else:
            break

    while True:
        cnpj = str(input("CNPJ: "))
        cnpj_limpo = "".join(filter(str.isdigit, cnpj))
        url = f"https://brasilapi.com.br/api/cnpj/v1/{cnpj_limpo}"
        console.print(f"[cyan]\nConsultando CNPJ {cnpj_limpo}, por favor aguarde...[/cyan]")
        
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                if cnpj_existe(cnpj_limpo):
                    console.print("[red]❌ Esse CNPJ já está cadastrado.[/red]")
                    aguardar(2)
                    continue
                else: 
                    console.print("[green]✔ CNPJ válido![/green]")
                    aguardar(1)
                    break
            else:
                console.print("[red]✖ CNPJ não encontrado ou inválido.[/red]")
                aguardar(2)
        except requests.exceptions.RequestException:
            console.print("[red]✖ Falha na conexão. Verifique sua internet.[/red]")
            aguardar(2)

    while True:
        telefone_ponto = str(input("Telefone (ex: 8199999-9999): "))
        numero_limpo_ponto = "".join(filter(str.isdigit, telefone_ponto))
        if len(numero_limpo_ponto) == 11:
            break  
        else:
            console.print("[red]❌ Número inválido, tente novamente.[/red]")

    while True:
        email_ponto = str(input("Email: "))
        if validar_email(email_ponto):
            if email_existe(email_ponto):
                console.print("[red]❌ Email já cadastrado, tente outro.[/red]")
                aguardar(2)
            else:
                break
        else: 
            console.print("[red]Email inválido, digite corretamente.[/red]")

    while True:
        confirmar_email_ponto = str(input("Confirme o email: "))
        if email_ponto == confirmar_email_ponto:
            break
        else:
            console.print("[yellow]⚠ Emails diferentes, tente novamente.[/yellow]")

    while True:
        console.print("[cyan]Senha: mínimo 8 caracteres, 1 número e 1 letra, sem especiais.[/cyan]")
        senha_ponto = str(input("Criar senha: ")) 
        resultado = validar_senha(senha_ponto)
        if resultado == "Aprovada!":
            console.print("[green]✔ Senha válida![/green]")
            break
        else:
            console.print(f"[red]{resultado}[/red]")

    while True:
        confirmar_senha_ponto = str(input("Confirme a senha: "))
        if senha_ponto != confirmar_senha_ponto:
            console.print("[yellow]⚠ Senhas diferentes, tente novamente.[/yellow]")
        else:
            console.print("[green]🔐 Senha confirmada![/green]")
            break

    endereco_formatado = endereco()

    while True:
        confirmar_cadastro_ponto = int(input("\nConfirmar cadastro? \n[1] Sim \n[2] Não\n"))
        if confirmar_cadastro_ponto == 1:
            pontos_existentes = carregar_pontos()
            novo_ponto = {
                "nome_ponto": nome_ponto,
                "cnpj": cnpj_limpo,
                "telefone": numero_limpo_ponto,
                "email": email_ponto,
                "senha": senha_ponto,
                "endereco": endereco_formatado,
            }
            pontos_existentes.append(novo_ponto)
            salvar_pontos(pontos_existentes)
            console.print(Panel.fit("[bold green]🎉 CADASTRO EFETIVADO COM SUCESSO![/bold green]", border_style="bright_green"))
            aguardar(2)
            return
        elif confirmar_cadastro_ponto == 2:
            reiniciar = int(input("Deseja reiniciar? [1] Sim [2] Não\n"))
            if reiniciar == 1:
                console.print("[cyan]🔄 Reiniciando cadastro...[/cyan]")
                aguardar(2)
                cadastro_ponto()
            else:
                break
        else:
            console.print("[red]❌ Insira um número válido.[/red]")

# =====================================================
#              CADASTRO DE USUÁRIO
# =====================================================

def cadastro_usuario():
    limpar_tela()
    console.print(Panel.fit("[bold cyan]🧍 CADASTRO DE USUÁRIO[/bold cyan]", border_style="bright_cyan"))

    while True:
        nome_usuario = str(input("Nome: "))
        if len(nome_usuario) < 5:
            console.print("[yellow]⚠ Nome muito curto, mínimo 5 caracteres.[/yellow]")
        else:
            break

    while True:
        cpf = str(input("\nCPF: "))
        cpf_limpo = "".join(filter(str.isdigit, cpf))
        if len(cpf_limpo) == 11:
            if cpf_existe(cpf_limpo):
                console.print("[red]❌ CPF já cadastrado![/red]")
                aguardar(2)
            else:
                console.print("[green]✔ CPF com formato válido![/green]")
                break
        else:
            console.print("[red]❌ CPF inválido, deve conter 11 números.[/red]")

    cidade_usuario = str(input("\nCidade: "))

    while True:
        telefone_usuario = str(input("\nTelefone (ex: 81999999999): "))
        numero_limpo_usuario = "".join(filter(str.isdigit, telefone_usuario))
        if len(numero_limpo_usuario) == 11:
            break  
        else:
            console.print("[red]❌ Número inválido, tente novamente.[/red]")

    while True:
        email_usuario = str(input("\nEmail: "))
        if validar_email(email_usuario):
            if email_existe(email_usuario):
                console.print("[red]❌ Email já cadastrado, tente outro.[/red]")
                aguardar(2)
            else: 
                console.print(Panel("[bold green]📧 Email válido![/bold green]", box=box.ROUNDED))
                break
        else: 
            console.print("[red]Email inválido, digite corretamente.[/red]")

    while True:
        confirmar_email_usuario = str(input("\nConfirme o email: "))
        if email_usuario == confirmar_email_usuario:
            break
        else:
            console.print("[yellow]⚠ Emails diferentes, tente novamente.[/yellow]")

    while True:
        console.print("\n[cyan]Senha: mínimo 8 caracteres, 1 número e 1 letra, sem especiais.[/cyan]")
        senha_usuario = str(input("Criar senha: ")) 
        resultado_senha_usuario = validar_senha(senha_usuario)
        if resultado_senha_usuario == "Aprovada!":
            break
        else:
            continue

    while True:
        confirmar_senha_usuario = str(input("\nConfirme a senha: "))
        if senha_usuario != confirmar_senha_usuario:
            console.print("[yellow]⚠ Senhas diferentes, tente novamente.[/yellow]")
        else:
            console.print("[green]🔐 Senha confirmada![/green]")
            break

    while True:
        confirmar_cadastro_usuario = int(input("\nConfirmar cadastro? \n[1] Sim \n[2] Não\n"))
        if confirmar_cadastro_usuario == 1:
            usuarios_existentes = carregar_usuarios()
            novo_usuario = {
                "nome": nome_usuario,
                "cpf": cpf_limpo,
                "cidade": cidade_usuario,
                "telefone": numero_limpo_usuario,
                "email": email_usuario,
                "senha": senha_usuario 
            }
            usuarios_existentes.append(novo_usuario)
            salvar_usuarios(usuarios_existentes)
            console.print(Panel.fit("[bold green]🎉 CADASTRO EFETIVADO COM SUCESSO![/bold green]", border_style="bright_green"))
            aguardar(2)
            return 
        elif confirmar_cadastro_usuario == 2:
            reiniciar_usuario = int(input("Deseja reiniciar? [1] Sim [2] Não\n"))
            if reiniciar_usuario == 1:
                console.print("[cyan]🔄 Reiniciando cadastro...[/cyan]")
                aguardar(2)
                cadastro_usuario()
            else:
                break
        else:
            console.print("[red]❌ Insira um número válido.[/red]")


def cadastro_reciclagem():
    pass  # placeholder

