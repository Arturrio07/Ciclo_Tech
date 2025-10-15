import json
from utils import limpar_tela, aguardar

def verificar_credenciais(email, senha):
    """
    Verifica se o email e a senha correspondem a um usuário no arquivo JSON.
    """
    try:
        with open('usuarios.json', 'r', encoding='utf-8') as file:
            usuarios = json.load(file)
            for usuario in usuarios:
                if usuario.get('email') == email and usuario.get('senha') == senha:
                    return True
    except (FileNotFoundError, json.JSONDecodeError):
        # Se o arquivo não existe ou está vazio/malformado, não há usuários para logar.
        return False
    return False

def menu_logado():
    """
    Exibe um menu simples para o usuário após o login bem-sucedido.
    """
    limpar_tela()
    print("______BEM-VINDO______\n")
    print("Você está logado no sistema!\n")
    # Aqui você pode adicionar mais funcionalidades para o usuário logado
    print("Pressione Enter para fazer logout...")
    input()
    print("Fazendo logout e voltando ao menu principal...")
    aguardar(2)

def login():
    """
    Gerencia o processo de login do usuário.
    """
    limpar_tela()
    print("______TELA DE LOGIN______\n")
    
    email = input("Digite seu email: ")
    senha = input("Digite sua senha: ")

    print("\nVerificando credenciais...")
    aguardar(2)

    if verificar_credenciais(email, senha):
        print("\nLogin realizado com sucesso!")
        aguardar(1)
        menu_logado()
    else:
        print("\nEmail ou senha incorretos.")
        print("Tente novamente ou realize o cadastro.")
        aguardar(3)