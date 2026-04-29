import customtkinter as ctk
from banco import buscar_pergunta, verificar_resposta, atualizar_senha


class TrocarSenha(ctk.CTkToplevel):
    def __init__(self, master, usuario):
        super().__init__(master)

        self.usuario = usuario

        self.title("Recuperar Senha")
        self.geometry("420x480")
        self.resizable(False, False)

        # 🔥 destaque
        self.grab_set()
        self.focus_force()

        # 🔥 container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=20, pady=20)

        # 🔥 card
        self.card = ctk.CTkFrame(self.container, corner_radius=25)
        self.card.pack(expand=True, fill="both")

        # 🔥 título
        self.titulo = ctk.CTkLabel(
            self.card,
            text="🔐 Redefinir senha",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        self.titulo.pack(pady=(25, 5))

        # 🔥 subtítulo
        self.subtitulo = ctk.CTkLabel(
            self.card,
            text="Responda a pergunta de segurança",
            text_color="#9a9a9a",
            font=ctk.CTkFont(size=13)
        )
        self.subtitulo.pack(pady=(0, 20))

        # 🔥 buscar pergunta
        pergunta = buscar_pergunta(usuario)
        pergunta = pergunta[0] if pergunta else "Pergunta não encontrada"

        # 🔥 label pergunta
        self.label_pergunta = ctk.CTkLabel(
            self.card,
            text=f"❓ {pergunta}",
            wraplength=300,
            font=ctk.CTkFont(size=13)
        )
        self.label_pergunta.pack(pady=(5, 15), padx=20)

        # 🔥 resposta
        self.resposta = ctk.CTkEntry(
            self.card,
            placeholder_text="💬 Sua resposta",
            height=45,
            corner_radius=12
        )
        self.resposta.pack(pady=10, padx=40, fill="x")

        # 🔥 nova senha
        self.nova_senha = ctk.CTkEntry(
            self.card,
            placeholder_text="🔒 Nova senha",
            show="*",
            height=45,
            corner_radius=12
        )
        self.nova_senha.pack(pady=10, padx=40, fill="x")

        # 🔥 confirmar senha
        self.confirmar = ctk.CTkEntry(
            self.card,
            placeholder_text="🔒 Confirmar senha",
            show="*",
            height=45,
            corner_radius=12
        )
        self.confirmar.pack(pady=10, padx=40, fill="x")

        # 🔥 status
        self.status = ctk.CTkLabel(
            self.card,
            text="",
            font=ctk.CTkFont(size=12),
            wraplength=280
        )
        self.status.pack(pady=10)

        # 🔥 botão principal (VERSÃO FINAL - maior)
        self.botao = ctk.CTkButton(
            self.card,
            text="Redefinir senha →",
            height=55,
            corner_radius=16,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1f6aa5",
            hover_color="#144870",
            command=self.alterar
        )
        self.botao.pack(pady=(0, 5), padx=20, fill="x")

        # 🔥 cancelar
        self.cancelar = ctk.CTkButton(
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
        self.cancelar.pack(pady=(5, 20), padx=40, fill="x")

    def alterar(self):
        resposta = self.resposta.get().strip()
        nova = self.nova_senha.get().strip()
        confirmar = self.confirmar.get().strip()

        if not resposta or not nova:
            self.status.configure(
                text="⚠️ Preencha todos os campos",
                text_color="#ff5555"
            )
            return

        if nova != confirmar:
            self.status.configure(
                text="❌ As senhas não coincidem",
                text_color="#ff5555"
            )
            return

        # 🔥 verifica resposta
        if not verificar_resposta(self.usuario, resposta):
            self.status.configure(
                text="❌ Resposta incorreta",
                text_color="#ff5555"
            )
            return

        # 🔥 feedback visual
        self.status.configure(
            text="✔ Redefinindo senha...",
            text_color="#2ecc71"
        )

        self.after(500, self.finalizar)

    def finalizar(self):
        atualizar_senha(self.usuario, self.nova_senha.get())

        self.status.configure(
            text="✅ Senha redefinida com sucesso!",
            text_color="#2ecc71"
        )

        self.after(1000, self.destroy)