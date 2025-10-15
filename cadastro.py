import json
from utils import limpar_tela, aguardar, validar_email, validar_senha

def cadastro():
    limpar_tela()
    print("______TELA DE CADASTRO______\n")

    while True:
        email = input("Digite seu email: ")
        if validar_email(email):
            break
        else:
            print("\nEmail inválido. Tente novamente.")
            aguardar(2)
            limpar_tela()

    while True:
        senha = input("Digite sua senha: ")
        status_senha = validar_senha(senha)
        if status_senha == "Aprovada!":
            break
        else:
            print(f"\nSenha inválida: {status_senha}")
            aguardar(2)
            limpar_tela()
            print(f"Email: {email}")

    novo_usuario = {"email": email, "senha": senha}

    try:
        # Tenta ler os usuários existentes
        try:
            with open('usuarios.json', 'r', encoding='utf-8') as file:
                usuarios = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Se o arquivo não existe ou está vazio, começa com uma lista vazia
            usuarios = []

        # Adiciona o novo usuário à lista
        usuarios.append(novo_usuario)

        # Salva a lista inteira de volta no arquivo
        with open('usuarios.json', 'w', encoding='utf-8') as file:
            json.dump(usuarios, file, indent=4, ensure_ascii=False)

        print("\nCadastro realizado com sucesso!")
        aguardar(2)

    except Exception as e:
        print(f"\nOcorreu um erro ao salvar seu cadastro: {e}")
        aguardar(3)