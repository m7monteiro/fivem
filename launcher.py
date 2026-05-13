import subprocess
import os
import sys
import base64
import ctypes
import time
import math
import random
import traceback

# Tenta importar bibliotecas necessárias, se falhar, avisa o usuário
try:
    import tkinter as tk
    from tkinter import messagebox
    import requests
except ImportError as e:
    # Se falhar aqui, tentamos usar o ctypes para mostrar uma mensagem de erro do Windows
    error_msg = f"Erro: Biblioteca faltando: {e}\nPor favor, instale usando: pip install requests"
    try:
        ctypes.windll.user32.MessageBoxW(0, error_msg, "Erro de Inicialização", 0x10)
    except:
        print(error_msg)
    sys.exit(1)

# ===== CONFIGURAÇÕES E SEGURANÇA =====
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

# Forçar Admin (Opcional - Remova se causar problemas no teste)
if not is_admin():
    try:
        # Se estiver no Windows, tenta elevar
        if os.name == 'nt':
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit()
    except Exception as e:
        print(f"Aviso: Não foi possível elevar para admin: {e}")

# ===== DADOS DO CHEAT =====
# Carregando de arquivo para não poluir o código e evitar erros de string gigante
try:
    # No ambiente do usuário, ele deve colar a string aqui ou manter o arquivo
    # Para esta entrega, vou embutir um marcador ou tentar ler se o arquivo existir
    if os.path.exists("base64.txt"):
        with open("base64.txt", "r") as f:
            CHEAT_BASE64 = f.read().strip()
    else:
        CHEAT_BASE64 = "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"
except Exception as e:
    CHEAT_BASE64 = ""
    print(f"Erro ao carregar base64: {e}")

# ===== URL DO GIST =====
URL_USUARIOS = "https://gist.githubusercontent.com/m7monteiro/bfa2949d06b09110b61cbbd49dcbf087/raw/clientes.txt"

def obter_diretorio_atual():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def carregar_usuarios_online():
    try:
        timestamp = int(time.time())
        url = f"{URL_USUARIOS}?t={timestamp}"
        headers = {"Cache-Control": "no-cache"}
        resposta = requests.get(url, timeout=10, headers=headers)
        resposta.raise_for_status()
        usuarios = {}
        for linha in resposta.text.splitlines():
            linha = linha.strip()
            if linha and ':' in linha:
                login, senha = linha.split(':', 1)
                usuarios[login.strip().lower()] = senha.strip()
        return usuarios
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Não foi possível carregar a lista de usuários.\nVerifique sua internet.\n\nDetalhes: {e}")
        return None

def extrair_e_executar():
    try:
        diretorio = obter_diretorio_atual()
        cheat_temp = os.path.join(diretorio, "temp_cheat.exe")
        
        # Tenta remover se já existir
        if os.path.exists(cheat_temp):
            try: os.remove(cheat_temp)
            except: pass
            
        if not CHEAT_BASE64:
            raise Exception("Dados do cheat (BASE64) não encontrados no código!")
            
        dados_cheat = base64.b64decode(CHEAT_BASE64)
        with open(cheat_temp, "wb") as f:
            f.write(dados_cheat)
            
        subprocess.Popen([cheat_temp])
        sys.exit()
    except Exception as e:
        messagebox.showerror("Erro Fatal", f"Falha ao iniciar o cheat:\n{e}")

# ============================================================
#  INTERFACE GRÁFICA 3D (LoginApp)
# ============================================================
class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("333 - M7STORE")
        self.root.geometry("520x580")
        self.root.resizable(False, False)
        self.root.configure(bg="#000000")
        
        # Centralizar
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()
        x = (screen_w // 2) - (520 // 2)
        y = (screen_h // 2) - (580 // 2)
        self.root.geometry(f"520x580+{x}+{y}")

        # Estado
        self.mouse_x, self.mouse_y = 260, 290
        self.tilt_x, self.tilt_y = 0.0, 0.0
        self.anim_frame = 0
        self.particles = []
        self.grid_offset = 0
        self.glow_phase = 0
        self.shake_frames = 0
        self.shake_dx = 0

        # Canvas de fundo
        self.bg_canvas = tk.Canvas(root, width=520, height=580, bg="#000000", highlightthickness=0)
        self.bg_canvas.place(x=0, y=0)

        # Inicializa partículas
        for _ in range(50):
            self.particles.append({
                'x': random.uniform(0, 520), 'y': random.uniform(0, 580),
                'vx': random.uniform(-0.3, 0.3), 'vy': random.uniform(-0.7, -0.2),
                'size': random.uniform(1, 2.5), 'alpha': random.uniform(0.3, 0.8),
                'color': random.choice(['#ff0000', '#880000', '#ff4444']),
                'life': random.uniform(0, 1)
            })

        # Borda neon (Fica ATRÁS do painel)
        self.border_canvas = tk.Canvas(root, width=368, height=428, bg="#000000", highlightthickness=0)
        self.border_canvas.place(x=76, y=76)

        # Frame do painel (Fica NA FRENTE da borda)
        self.panel_frame = tk.Frame(root, bg="#0a0a0a", bd=0)
        self.panel_frame.place(x=80, y=80, width=360, height=420)

        self._build_ui()
        self.root.bind("<Motion>", self._on_mouse_move)
        self._animate()

    def _build_ui(self):
        # Logo com efeito de sombra
        self.logo_canvas = tk.Canvas(self.panel_frame, width=360, height=110, bg="#0a0a0a", highlightthickness=0)
        self.logo_canvas.pack(pady=(10, 0))
        self.logo_shadow = self.logo_canvas.create_text(183, 58, text="333", font=("Impact", 75, "bold"), fill="#220000")
        self.logo_text = self.logo_canvas.create_text(180, 55, text="333", font=("Impact", 75, "bold"), fill="#ff0000")

        tk.Label(self.panel_frame, text="▸ ACESSO RESTRITO ◂", font=("Courier", 10, "bold"), bg="#0a0a0a", fg="#880000").pack()
        
        # Inputs Estilizados
        tk.Label(self.panel_frame, text="USUÁRIO", font=("Courier", 9, "bold"), bg="#0a0a0a", fg="#ff0000").pack(anchor="w", padx=45, pady=(15, 0))
        self.entry_login = tk.Entry(self.panel_frame, font=("Courier", 12), bg="#151515", fg="#ff4444", insertbackground="#ff0000", relief="flat", bd=10)
        self.entry_login.pack(fill="x", padx=45)
        self.entry_login.focus()

        tk.Label(self.panel_frame, text="SENHA", font=("Courier", 9, "bold"), bg="#0a0a0a", fg="#ff0000").pack(anchor="w", padx=45, pady=(10, 0))
        self.entry_senha = tk.Entry(self.panel_frame, font=("Courier", 12), bg="#151515", fg="#ff4444", insertbackground="#ff0000", relief="flat", bd=10, show="●")
        self.entry_senha.pack(fill="x", padx=45)
        self.entry_senha.bind("<Return>", lambda e: self._fazer_login())

        # Botão com efeito
        self.btn = tk.Button(self.panel_frame, text="▶ ENTRAR", font=("Courier", 13, "bold"), bg="#ff0000", fg="black", activebackground="#cc0000", activeforeground="white", relief="flat", cursor="hand2", command=self._fazer_login)
        self.btn.pack(pady=25, ipadx=50, ipady=8)

        tk.Label(self.panel_frame, text="© M7STORE 2026", font=("Courier", 7), bg="#0a0a0a", fg="#330000").pack(side="bottom", pady=10)

    def _on_mouse_move(self, event):
        self.mouse_x, self.mouse_y = event.x, event.y

    def _fazer_login(self):
        login = self.entry_login.get().strip().lower()
        senha = self.entry_senha.get().strip()
        if not login or not senha:
            self.shake_frames = 10
            messagebox.showwarning("Aviso", "Preencha todos os campos!")
            return
        
        usuarios = carregar_usuarios_online()
        if usuarios and login in usuarios and usuarios[login] == senha:
            extrair_e_executar()
        else:
            self.shake_frames = 10
            messagebox.showerror("Erro", "Login ou senha incorretos!")

    def _animate(self):
        self.anim_frame += 1
        self.glow_phase += 0.05
        self.grid_offset = (self.grid_offset + 0.5) % 40

        # Parallax
        target_tx = (self.mouse_x - 260) / 260 * 10
        target_ty = (self.mouse_y - 290) / 290 * 6
        self.tilt_x += (target_tx - self.tilt_x) * 0.05
        self.tilt_y += (target_ty - self.tilt_y) * 0.05

        # Shake
        if self.shake_frames > 0:
            self.shake_dx = random.randint(-5, 5)
            self.shake_frames -= 1
        else: self.shake_dx = 0

        px, py = 80 + self.tilt_x + self.shake_dx, 80 + self.tilt_y
        self.border_canvas.place(x=px-4, y=py-4)
        self.panel_frame.place(x=px, y=py)
        self.panel_frame.lift() # Garante que o painel fique sempre no topo

        # Background
        self.bg_canvas.delete("bg")
        # Grade
        for i in range(10):
            y = 290 + (i/10)**2 * 290
            self.bg_canvas.create_line(0, y, 520, y, fill="#220000", tags="bg")
        
        # Partículas
        for p in self.particles:
            p['y'] += p['vy']
            if p['y'] < 0: p['y'] = 580
            self.bg_canvas.create_oval(p['x'], p['y'], p['x']+p['size'], p['y']+p['size'], fill=p['color'], outline="", tags="bg")

        # Glow Logo
        glow = int(150 + 105 * math.sin(self.glow_phase))
        self.logo_canvas.itemconfig(self.logo_text, fill=f"#{glow:02x}0000")

        self.root.after(16, self._animate)

# ============================================================
#  INICIALIZAÇÃO COM TRATAMENTO DE ERRO GLOBAL
# ============================================================
if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = LoginApp(root)
        root.mainloop()
    except Exception as e:
        # Se o programa crashar, mostra o erro em uma janela antes de fechar
        error_details = traceback.format_exc()
        try:
            # Tenta usar o próprio tkinter se ele ainda estiver vivo
            messagebox.showerror("Erro Crítico", f"Ocorreu um erro inesperado:\n\n{e}\n\nDetalhes:\n{error_details}")
        except:
            # Fallback para o Windows
            ctypes.windll.user32.MessageBoxW(0, f"Erro Crítico:\n{e}\n\n{error_details}", "Crash do Sistema", 0x10)
