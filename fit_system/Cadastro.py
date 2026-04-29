import customtkinter as ctk
from banco import cadastrar_usuario


class CadastroApp(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Cadastro")
        self.geometry("550x800")
        self.resizable(False, False)

        # 🔥 destaque da janela
        self.grab_set()
        self.focus_force()
        self.lift()

        # 🔥 container
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(expand=True, fill="both", padx=20, pady=20)

        # 🔥 card principal
        self.card = ctk.CTkFrame(self.container, corner_radius=25)
        self.card.pack(expand=True, fill="both")

        # 🔥 título
        self.titulo = ctk.CTkLabel(
            self.card,
            text="📝 Criar Conta",
            font=ctk.CTkFont(size=26, weight="bold")
        )
        self.titulo.pack(pady=(25, 5))

        # 🔥 subtítulo
        self.subtitulo = ctk.CTkLabel(
            self.card,
            text="Preencha os dados abaixo",
            text_color="#9a9a9a",
            font=ctk.CTkFont(size=13)
        )
        self.subtitulo.pack(pady=(0, 20))

        # 🔥 campos
        self.nome = ctk.CTkEntry(
            self.card,
            placeholder_text="👤 Nome completo",
            height=45,
            corner_radius=12
        )
        self.nome.pack(pady=8, padx=40, fill="x")

        self.usuario = ctk.CTkEntry(
            self.card,
            placeholder_text="🧑 Usuário",
            height=45,
            corner_radius=12
        )
        self.usuario.pack(pady=8, padx=40, fill="x")

        self.senha = ctk.CTkEntry(
            self.card,
            placeholder_text="🔒 Senha",
            show="*",
            height=45,
            corner_radius=12
        )
        self.senha.pack(pady=8, padx=40, fill="x")

        self.confirmar_senha = ctk.CTkEntry(
            self.card,
            placeholder_text="🔒 Confirmar senha",
            show="*",
            height=45,
            corner_radius=12
        )
        self.confirmar_senha.pack(pady=8, padx=40, fill="x")

        self.pergunta = ctk.CTkEntry(
            self.card,
            placeholder_text="❓ Pergunta de segurança",
            height=45,
            corner_radius=12
        )
        self.pergunta.pack(pady=8, padx=40, fill="x")

        self.resposta = ctk.CTkEntry(
            self.card,
            placeholder_text="💬 Resposta",
            height=45,
            corner_radius=12
        )
        self.resposta.pack(pady=8, padx=40, fill="x")

        # 🔥 tipo de usuário
        self.tipo_usuario = ctk.CTkOptionMenu(
            self.card,
            values=["Usuário", "Administrador"],
            height=45,
            corner_radius=12
        )
        self.tipo_usuario.set("Usuário")
        self.tipo_usuario.pack(pady=10, padx=40, fill="x")

        # 🔥 botão cadastrar
        self.botao = ctk.CTkButton(
            self.card,
            text="Cadastrar →",
            height=50,
            corner_radius=15,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="#1f6aa5",
            hover_color="#144870",
            command=self.cadastrar
        )
        self.botao.pack(pady=(20, 10), padx=40, fill="x")

            # 🔥 botão voltar
        self.voltar = ctk.CTkButton(
            self.card,
            text="← Voltar",
            height=40,
            corner_radius=12,
            fg_color="transparent",
            border_width=1,
            border_color="#444",
            hover_color="#2a2a2a",
            command=self.destroy
        )
        self.voltar.pack(pady=(0, 5), padx=40, fill="x")

        # 🔥 status
        self.status = ctk.CTkLabel(
            self.card,
            text="",
            font=ctk.CTkFont(size=12),
            wraplength=300
        )
        self.status.pack(pady=(5, 15))

    def cadastrar(self):
        nome = self.nome.get().strip()
        usuario = self.usuario.get().strip()
        senha = self.senha.get().strip()
        confirmar = self.confirmar_senha.get().strip()
        pergunta = self.pergunta.get().strip()
        resposta = self.resposta.get().strip()
        tipo = self.tipo_usuario.get()

        # 🔥 converter tipo
        tipo = "admin" if tipo == "Administrador" else "usuario"

        if not nome or not usuario or not senha or not pergunta or not resposta:
            self.status.configure(
                text="⚠️ Preencha todos os campos",
                text_color="#ff5555"
            )
            return

        if senha != confirmar:
            self.status.configure(
                text="❌ As senhas não coincidem",
                text_color="#ff5555"
            )
            return

        # 🔥 salvar
        resultado = cadastrar_usuario(nome, usuario, senha, pergunta, resposta, tipo)

        if resultado == True:
            self.status.configure(
                text="✅ Usuário cadastrado com sucesso!",
                text_color="#2ecc71"
            )

            # limpar campos
            self.nome.delete(0, "end")
            self.usuario.delete(0, "end")
            self.senha.delete(0, "end")
            self.confirmar_senha.delete(0, "end")
            self.pergunta.delete(0, "end")
            self.resposta.delete(0, "end")

        elif resultado == "existe":
            self.status.configure(
                text="❌ Usuário já existe",
                text_color="#ff5555"
            )
        else:
            self.status.configure(
                text="❌ Erro ao cadastrar",
                text_color="#ff5555"
            )