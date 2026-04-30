import subprocess
import os
import sys

# Nome do seu .exe do cheat (mesmo nome que estará na pasta)
CHEAT_EXE = "cheat.exe"

def carregar_usuarios():
    usuarios = {}
    try:
        # Tenta ler o arquivo de usuarios.txt que está na mesma pasta
        with open("usuarios.txt", 'r', encoding='utf-8') as f:
            for linha in f:
                linha = linha.strip()
                if linha and not linha.startswith('#'):
                    login, senha = linha.split(':')
                    usuarios[login.lower()] = senha
    except FileNotFoundError:
        # Se não achar, cria um padrão
        with open("usuarios.txt", 'w') as f:
            f.write("admin:123456\n")
        return {"admin": "123456"}
    return usuarios

def fazer_login():
    print("\n" + "="*40)
    print("    ACESSO AO CHEAT")
    print("="*40)
    
    usuarios = carregar_usuarios()
    tentativas = 0
    
    while tentativas < 3:
        print("\nInsira suas credenciais:")
        login = input("Login: ").strip().lower()
        senha = input("Senha: ").strip()
        
        if login in usuarios and usuarios[login] == senha:
            print(f"\n✅ Bem-vindo, {login}!")
            return True
        else:
            tentativas += 1
            print(f"❌ Falhou! Tentativas restantes: {3 - tentativas}")
    
    print("🚫 Acesso Bloqueado.")
    return False

def main():
    if fazer_login():
        # Verifica se o cheat está ali do lado
        if os.path.exists(CHEAT_EXE):
            print(f"Iniciando {CHEAT_EXE}...")
            subprocess.run([CHEAT_EXE])
        else:
            print(f"Erro: Não encontrei o arquivo {CHEAT_EXE}")
            input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
