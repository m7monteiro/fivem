import sys
import ctypes

# Elevar privilégios
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if not is_admin():
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
    sys.exit()

# Teste de importação
try:
    from keyauth import KeyAuth   # <--- LINHA CORRETA
    print("✅ KeyAuth importado com sucesso!")
    print("Versão:", KeyAuth.__version__ if hasattr(KeyAuth, '__version__') else 'desconhecida')
    input("Pressione Enter para sair...")
except Exception as e:
    print(f"❌ Erro ao importar: {e}")
    input("Pressione Enter para sair...")
