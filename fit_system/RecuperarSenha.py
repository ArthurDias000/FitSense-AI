import customtkinter as ctk
from troca_senha import TrocarSenha
from banco import usuario_existe


class RecuperarSenha(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master)

        self.title("Recuperar senha")
        self.geometry("400x340")
        self.resizable(False, False)

        # 🔥 destaque da janela
        self.grab_set()
        self.focus_force()

        # 🔥 container principal
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=20, pady=20)

        # 🔥 card central
        self.card = ctk.CTkFrame(self.container, corner_radius=25)
        self.card.pack(expand=True, fill="both")

        # 🔥 título com ícone
        self.titulo = ctk.CTkLabel(
            self.card,
            text="🔐 Recuperar senha",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.titulo.pack(pady=(25, 5))

        # 🔥 subtítulo
        self.subtitulo = ctk.CTkLabel(
            self.card,
            text="Informe seu usuário para continuar",
            text_color="#9a9a9a",
            font=ctk.CTkFont(size=13)
        )
        self.subtitulo.pack(pady=(0, 25))

        # 🔥 campo com "efeito moderno"
        self.usuario_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="👤 Usuário",
            height=45,
            corner_radius=12,
            border_width=1
        )
        self.usuario_entry.pack(pady=10, padx=40, fill="x")

        # 🔥 status bonito
        self.status = ctk.CTkLabel(
            self.card,
            text="",
            font=ctk.CTkFont(size=12),
            wraplength=250
        )
        self.status.pack(pady=8)

        # 🔥 botão principal
        self.botao = ctk.CTkButton(
            self.card,
            text="Continuar →",
            height=45,
            corner_radius=14,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#1f6aa5",
            hover_color="#144870",
            command=self.continuar
        )
        self.botao.pack(pady=(20, 10), padx=40, fill="x")

        # 🔥 botão voltar (extra UX)
        self.voltar = ctk.CTkButton(
            self.card,
            text="Cancelar",
            height=35,
            corner_radius=10,
            fg_color="transparent",
            border_width=1,
            border_color="#444",
            hover_color="#2a2a2a",
            command=self.destroy
        )
        self.voltar.pack(pady=(5, 20), padx=40, fill="x")

        # 🔥 ENTER funciona
        self.bind("<Return>", lambda e: self.continuar())

    def continuar(self):
        usuario = self.usuario_entry.get().strip()

        if not usuario:
            self.status.configure(
                text="⚠️ Digite o usuário",
                text_color="#ff5555"
            )
            return

        # 🔥 verifica usuário
        if not usuario_existe(usuario):
            self.status.configure(
                text="❌ Usuário não encontrado",
                text_color="#ff5555"
            )
            return

        # 🔥 feedback sucesso rápido
        self.status.configure(
            text="✔ Usuário encontrado!",
            text_color="#2ecc71"
        )

        # pequena pausa visual (efeito profissional)
        self.after(500, lambda: self.ir_para_troca(usuario))

    def ir_para_troca(self, usuario):
        self.destroy()
        self.trocar = TrocarSenha(self.master, usuario)