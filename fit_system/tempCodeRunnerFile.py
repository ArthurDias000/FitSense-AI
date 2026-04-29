import customtkinter as ctk
from Cadastro import CadastroApp
from banco import verificar_login, criar_tabela
from RecuperarSenha import RecuperarSenha
from Tela_Guia import TelaGuia

criar_tabela()

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class LoginApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("FitSense AI")
        self.geometry("1000x600")
        self.resizable(False, False)
        self.configure(fg_color="#0b0f19")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # =========================
        # PAINEL ESQUERDO
        # =========================
        self.left_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="#101827"
        )
        self.left_frame.grid(row=0, column=0, sticky="nsew")

        self.logo_box = ctk.CTkFrame(
            self.left_frame,
            width=70,
            height=70,
            corner_radius=20,
            fg_color="#2563eb"
        )
        self.logo_box.place(relx=0.5, rely=0.25, anchor="center")
        self.logo_box.pack_propagate(False)

        ctk.CTkLabel(
            self.logo_box,
            text="AI",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="white"
        ).pack(expand=True)

        self.left_title = ctk.CTkLabel(
            self.left_frame,
            text="FitSense AI",
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color="#ffffff"
        )
        self.left_title.place(relx=0.5, rely=0.40, anchor="center")

        self.left_subtitle = ctk.CTkLabel(
            self.left_frame,
            text="Previsão inteligente de cancelamento\npara academias.",
            font=ctk.CTkFont(size=15),
            text_color="#94a3b8",
            justify="center"
        )
        self.left_subtitle.place(relx=0.5, rely=0.50, anchor="center")

        self.feature_box = ctk.CTkFrame(
            self.left_frame,
            corner_radius=18,
            fg_color="#0f172a",
            border_width=1,
            border_color="#1e293b"
        )
        self.feature_box.place(relx=0.5, rely=0.72, anchor="center")

        ctk.CTkLabel(
            self.feature_box,
            text="📊 Dashboard   🔮 IA   📂 Dados",
            font=ctk.CTkFont(size=13),
            text_color="#cbd5e1"
        ).pack(padx=25, pady=18)

        # =========================
        # PAINEL DIREITO
        # =========================
        self.right_area = ctk.CTkFrame(
            self,
            fg_color="#0b0f19",
            corner_radius=0
        )
        self.right_area.grid(row=0, column=1, sticky="nsew")

        self.card = ctk.CTkFrame(
            self.right_area,
            width=380,
            height=460,
            corner_radius=28,
            fg_color="#111827",
            border_width=1,
            border_color="#1f2937"
        )
        self.card.place(relx=0.5, rely=0.5, anchor="center")
        self.card.pack_propagate(False)

        ctk.CTkLabel(
            self.card,
            text="Entrar na conta",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#ffffff"
        ).pack(pady=(35, 5))

        ctk.CTkLabel(
            self.card,
            text="Acesse o painel do sistema",
            font=ctk.CTkFont(size=13),
            text_color="#94a3b8"
        ).pack(pady=(0, 25))

        self.username_entry = ctk.CTkEntry(
            self.card,
            placeholder_text="Usuário",
            height=48,
            corner_radius=14,
            fg_color="#0f172a",
            border_color="#334155",
            border_width=1,
            font=ctk.CTkFont(size=14)
        )
        self.username_entry.pack(padx=35, pady=8, fill="x")

        self.mostrar_senha = False

        self.password_frame = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )
        self.password_frame.pack(padx=35, pady=8, fill="x")
        self.password_frame.grid_columnconfigure(0, weight=1)

        self.password_entry = ctk.CTkEntry(
            self.password_frame,
            placeholder_text="Senha",
            show="*",
            height=48,
            corner_radius=14,
            fg_color="#0f172a",
            border_color="#334155",
            border_width=1,
            font=ctk.CTkFont(size=14)
        )
        self.password_entry.grid(row=0, column=0, sticky="ew")

        self.toggle_button = ctk.CTkButton(
            self.password_frame,
            text="👁",
            width=48,
            height=48,
            corner_radius=14,
            fg_color="#1e293b",
            hover_color="#334155",
            command=self.toggle_senha
        )
        self.toggle_button.grid(row=0, column=1, padx=(8, 0))

        self.status = ctk.CTkLabel(
            self.card,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.status.pack(pady=(5, 0))

        self.login_button = ctk.CTkButton(
            self.card,
            text="Entrar",
            height=48,
            corner_radius=14,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.login
        )
        self.login_button.pack(padx=35, pady=(18, 12), fill="x")

        self.links_frame = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )
        self.links_frame.pack(pady=5)

        self.forgot_label = ctk.CTkLabel(
            self.links_frame,
            text="Esqueceu a senha?",
            text_color="#93c5fd",
            cursor="hand2",
            font=ctk.CTkFont(size=13)
        )
        self.forgot_label.pack(pady=4)
        self.forgot_label.bind("<Button-1>", self.abrir_recuperacao)

        self.create_account_label = ctk.CTkLabel(
            self.links_frame,
            text="Criar nova conta",
            text_color="#ffffff",
            cursor="hand2",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.create_account_label.pack(pady=4)
        self.create_account_label.bind("<Button-1>", self.abrir_cadastro)

        ctk.CTkLabel(
            self.card,
            text="© 2026 FitSense AI",
            font=ctk.CTkFont(size=10),
            text_color="#64748b"
        ).pack(side="bottom", pady=18)

        self.bind("<Return>", lambda e: self.login())
        self.username_entry.focus()

    def toggle_senha(self):
        self.mostrar_senha = not self.mostrar_senha

        if self.mostrar_senha:
            self.password_entry.configure(show="")
            self.toggle_button.configure(text="🙈")
        else:
            self.password_entry.configure(show="*")
            self.toggle_button.configure(text="👁")

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            self.status.configure(
                text="⚠️ Preencha todos os campos",
                text_color="#f87171"
            )
            return

        resultado = verificar_login(username, password)

        if resultado:
            tipo_usuario = resultado[6]
            self.status.configure(
                text="✔ Login realizado!",
                text_color="#22c55e"
            )
            self.after(500, lambda: self.abrir_sistema(username, tipo_usuario))
        else:
            self.status.configure(
                text="❌ Usuário ou senha incorretos",
                text_color="#f87171"
            )

    def abrir_sistema(self, username, tipo_usuario):
        self.withdraw()
        self.tela = TelaGuia(self, usuario=username, tipo=tipo_usuario)
        self.tela.protocol("WM_DELETE_WINDOW", self.voltar_login)
        self.tela.deiconify()

    def voltar_login(self):
        self.tela.destroy()
        self.deiconify()

    def abrir_cadastro(self, event=None):
        if hasattr(self, "cadastro_window") and self.cadastro_window.winfo_exists():
            self.cadastro_window.focus()
            return

        self.cadastro_window = CadastroApp(self)

    def abrir_recuperacao(self, event=None):
        self.recuperar = RecuperarSenha(self)


if __name__ == "__main__":
    app = LoginApp()
    app.mainloop()