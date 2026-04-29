import customtkinter as ctk
from ia_modelo import prever_cancelamento, treinar_modelo
from tela_previsao import TelaPrevisao
from tkinter import filedialog
from collections import Counter
from banco import listar_usuarios
from tela_usuarios import TelaUsuarios


from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


ctk.set_appearance_mode("dark")


class TelaGuia(ctk.CTkToplevel):
    def __init__(self, master=None, usuario=None, tipo=None):
        super().__init__(master)

        self.master = master
        self.usuario = usuario
        self.tipo = tipo
        self.dados = None

        self.title("FitSense AI")
        self.geometry(f"{self.winfo_screenwidth()}x{self.winfo_screenheight()}")
        self.configure(fg_color="#080b12")

        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.fechar_tela)

        self.sidebar = ctk.CTkFrame(self, width=270, fg_color="#020617", corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        ctk.CTkLabel(
            self.sidebar,
            text="FitSense AI",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#38bdf8"
        ).pack(pady=(38, 6))

        ctk.CTkLabel(
            self.sidebar,
            text="Inteligência para retenção",
            text_color="#64748b",
            font=ctk.CTkFont(size=13)
        ).pack(pady=(0, 25))

        user_card = ctk.CTkFrame(
            self.sidebar,
            fg_color="#0f172a",
            corner_radius=18,
            border_width=1,
            border_color="#1e293b"
        )
        user_card.pack(fill="x", padx=18, pady=(0, 25))

        ctk.CTkLabel(
            user_card,
            text=f"👤 {self.usuario}",
            font=ctk.CTkFont(size=15, weight="bold"),
            text_color="#e5e7eb"
        ).pack(anchor="w", padx=15, pady=(12, 2))

        ctk.CTkLabel(
            user_card,
            text=f"Perfil: {self.tipo}",
            text_color="#94a3b8",
            font=ctk.CTkFont(size=12)
        ).pack(anchor="w", padx=15, pady=(0, 12))

        def menu_btn(texto, comando=None):
            return ctk.CTkButton(
                self.sidebar,
                text=texto,
                height=46,
                corner_radius=14,
                fg_color="transparent",
                hover_color="#1e293b",
                anchor="w",
                command=comando,
                font=ctk.CTkFont(size=14)
            )

        menu_btn("🏠 Início", self.mostrar_inicio).pack(fill="x", padx=18, pady=5)
        menu_btn("🔮 Nova previsão", self.abrir_previsao).pack(fill="x", padx=18, pady=5)
        menu_btn("📂 Importar dados", self.importar_dados).pack(fill="x", padx=18, pady=5)
        menu_btn("➕ Cadastrar aluno", self.abrir_cadastro_aluno).pack(fill="x", padx=18, pady=5)
        menu_btn("📋 Listar alunos", self.abrir_lista_alunos).pack(fill="x", padx=18, pady=5)

        if self.tipo and self.tipo.lower() == "admin":
            menu_btn("🧑‍💼 Usuários", self.abrir_usuarios).pack(fill="x", padx=18, pady=5)

        ctk.CTkButton(
            self.sidebar,
            text="🚪 Sair",
            height=46,
            corner_radius=14,
            fg_color="#dc2626",
            hover_color="#991b1b",
            command=self.fechar_tela
        ).pack(side="bottom", fill="x", padx=18, pady=25)

        self.content = ctk.CTkScrollableFrame(self, fg_color="#080b12")
        self.content.pack(expand=True, fill="both", padx=32, pady=32)

        self.mostrar_inicio()

    def limpar_tela(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def mostrar_inicio(self):
        self.limpar_tela()

        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.pack(fill="x")

        ctk.CTkLabel(
            header,
            text=f"Olá, {self.usuario} 👋",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w")

        ctk.CTkLabel(
            header,
            text="Painel inteligente de retenção de clientes",
            text_color="#94a3b8",
            font=ctk.CTkFont(size=15)
        ).pack(anchor="w", pady=(4, 24))

        self.cards = ctk.CTkFrame(self.content, fg_color="transparent")
        self.cards.pack(fill="x")

        self.mostrar_cards()
        self.mostrar_graficos()

    def importar_dados(self):
        caminho = filedialog.askopenfilename(
            title="Selecionar CSV",
            filetypes=[("CSV", "*.csv")]
        )

        if caminho:
            try:
                self.dados = treinar_modelo(caminho)
                self.mostrar_inicio()
            except Exception as e:
                self.mostrar_status(f"Erro: {e}", "#ef4444")

    def calcular_riscos(self, dados):
        return [
            prever_cancelamento(
                row["atraso"],
                row["satisfacao"],
                row["personal"],
                row["freq"],
                row["tempo"],
                row["idade"],
                row["valor"]
            )["risco"]
            for _, row in dados.iterrows()
        ]

    def mostrar_cards(self):
        for widget in self.cards.winfo_children():
            widget.destroy()

        if self.dados is None:
            alto = medio = baixo = total_clientes = 0
        else:
            riscos = Counter(self.calcular_riscos(self.dados))
            alto = riscos.get("ALTO", 0)
            medio = riscos.get("MÉDIO", 0)
            baixo = riscos.get("BAIXO", 0)
            total_clientes = len(self.dados)

        total = max(1, alto + medio + baixo)

        def card(titulo, valor, cor, proporcao):
            shadow = ctk.CTkFrame(
                self.cards,
                fg_color="#020617",
                corner_radius=28
            )
            shadow.pack(side="left", padx=20, pady=10)

            frame = ctk.CTkFrame(
                shadow,
                width=270,
                height=160,
                corner_radius=24,
                fg_color="#0f172a",
                border_width=1,
                border_color="#1e293b"
            )
            frame.pack(padx=2, pady=2)
            frame.pack_propagate(False)

            glow = ctk.CTkFrame(
                frame,
                height=4,
                fg_color=cor
            )
            glow.pack(fill="x", side="top")

            ctk.CTkLabel(
                frame,
                text=titulo,
                text_color="#94a3b8",
                font=ctk.CTkFont(size=13)
            ).pack(anchor="w", padx=18, pady=(14, 2))

            ctk.CTkLabel(
                frame,
                text=str(valor),
                text_color=cor,
                font=ctk.CTkFont(size=38, weight="bold")
            ).pack(anchor="w", padx=18)

            barra_bg = ctk.CTkFrame(
                frame,
                height=8,
                fg_color="#1e293b",
                corner_radius=20
            )
            barra_bg.pack(fill="x", padx=18, pady=(14, 4))

            barra = ctk.CTkFrame(
                barra_bg,
                height=8,
                width=int(200 * proporcao),
                fg_color=cor,
                corner_radius=20
            )
            barra.pack(side="left")

            porcento = int(proporcao * 100)

            ctk.CTkLabel(
                frame,
                text=f"{porcento}%",
                text_color="#64748b",
                font=ctk.CTkFont(size=11)
            ).pack(anchor="e", padx=18, pady=(0, 10))

        card("🔴 Risco Alto", alto, "#ef4444", alto / total)
        card("🟠 Risco Médio", medio, "#f59e0b", medio / total)
        card("🟢 Risco Baixo", baixo, "#22c55e", baixo / total)
        card("👥 Clientes", total_clientes, "#38bdf8", 1)

    def mostrar_graficos(self):
        area = ctk.CTkFrame(
            self.content,
            fg_color="#0f172a",
            corner_radius=26,
            border_width=1,
            border_color="#1e293b"
        )
        area.pack(fill="both", expand=True, pady=24)

        ctk.CTkLabel(
            area,
            text="📊 Dashboard Inteligente",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w", padx=25, pady=(22, 6))

        ctk.CTkLabel(
            area,
            text="Análise visual dos alunos, riscos, retenção e comportamento financeiro.",
            text_color="#94a3b8",
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", padx=25, pady=(0, 15))

        if self.dados is None:
            ctk.CTkLabel(
                area,
                text="📂 Importe um CSV para visualizar os gráficos.",
                text_color="#94a3b8",
                font=ctk.CTkFont(size=15)
            ).pack(anchor="w", padx=25, pady=(5, 25))
            return

        colunas = ["mes", "status", "atraso", "satisfacao", "personal", "freq", "tempo", "idade", "valor"]

        for coluna in colunas:
            if coluna not in self.dados.columns:
                ctk.CTkLabel(
                    area,
                    text=f"CSV inválido: coluna ausente '{coluna}'",
                    text_color="#ef4444"
                ).pack(anchor="w", padx=25, pady=10)
                return

        dados = self.dados.copy()
        dados["status"] = dados["status"].astype(str).str.lower()
        dados["risco"] = self.calcular_riscos(dados)

        mapa = {"BAIXO": 1, "MÉDIO": 2, "ALTO": 3}
        dados["risco_num"] = dados["risco"].map(mapa)

        grid = ctk.CTkFrame(area, fg_color="transparent")
        grid.pack(fill="both", expand=True, padx=18, pady=18)

        for i in range(3):
            grid.grid_columnconfigure(i, weight=1)

        def criar_fig(titulo):
            fig = Figure(figsize=(4.7, 3.1), dpi=100)
            fig.patch.set_facecolor("#111827")

            ax = fig.add_subplot(111)
            ax.set_facecolor("#111827")
            ax.set_title(titulo, color="white", fontsize=12, fontweight="bold")
            ax.tick_params(colors="#cbd5e1")

            ax.spines["bottom"].set_color("#334155")
            ax.spines["left"].set_color("#334155")
            ax.spines["top"].set_visible(False)
            ax.spines["right"].set_visible(False)

            return fig, ax

        def inserir(fig, row, col):
            frame = ctk.CTkFrame(
                grid,
                fg_color="#111827",
                corner_radius=22,
                border_width=1,
                border_color="#1e293b"
            )
            frame.grid(row=row, column=col, padx=12, pady=12, sticky="nsew")

            canvas = FigureCanvasTkAgg(fig, master=frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True, padx=12, pady=12)

        ativos = dados[dados["status"] == "ativo"]
        cont = ativos["mes"].value_counts().sort_index()

        fig, ax = criar_fig("Clientes Ativos por Mês")
        ax.bar(cont.index, cont.values, color="#38bdf8")
        ax.set_ylabel("Clientes", color="#cbd5e1")
        ax.tick_params(axis="x", rotation=25)
        inserir(fig, 0, 0)

        status = dados["status"].value_counts()

        fig, ax = criar_fig("Ativos x Inativos")
        ax.pie(
            status.values,
            labels=status.index,
            autopct="%1.0f%%",
            colors=["#22c55e", "#ef4444"],
            textprops={"color": "white"}
        )
        inserir(fig, 0, 1)

        risco = dados["risco"].value_counts()
        ordem = ["ALTO", "MÉDIO", "BAIXO"]
        valores = [risco.get("ALTO", 0), risco.get("MÉDIO", 0), risco.get("BAIXO", 0)]

        fig, ax = criar_fig("Distribuição de Risco")
        ax.bar(ordem, valores, color=["#ef4444", "#f59e0b", "#22c55e"])
        ax.set_ylabel("Clientes", color="#cbd5e1")
        inserir(fig, 0, 2)

        risco_mes = dados.groupby("mes")["risco_num"].mean()

        fig, ax = criar_fig("Risco Médio por Mês")
        ax.plot(risco_mes.index, risco_mes.values, marker="o", color="#a855f7", linewidth=2)
        ax.set_ylabel("Risco", color="#cbd5e1")
        ax.tick_params(axis="x", rotation=25)
        inserir(fig, 1, 0)

        fig, ax = criar_fig("Frequência vs Risco")
        ax.scatter(dados["freq"], dados["risco_num"], color="#38bdf8", alpha=0.8)
        ax.set_xlabel("Frequência", color="#cbd5e1")
        ax.set_ylabel("Risco", color="#cbd5e1")
        inserir(fig, 1, 1)

        valor_mes = dados.groupby("mes")["valor"].mean()

        fig, ax = criar_fig("Valor Médio por Mês")
        ax.plot(valor_mes.index, valor_mes.values, marker="o", color="#f59e0b", linewidth=2)
        ax.set_ylabel("R$", color="#cbd5e1")
        ax.tick_params(axis="x", rotation=25)
        inserir(fig, 1, 2)

    def abrir_previsao(self):
        TelaPrevisao(self)

    def abrir_usuarios(self):
        if self.tipo.lower() != "admin":
            self.mostrar_status("❌ Acesso negado. Apenas administradores.", "#ef4444")
            return
        
        TelaUsuarios(self)

    def abrir_cadastro_aluno(self):
        from CadastrarAluno import CadastrarAluno
        CadastrarAluno(self)

    def abrir_lista_alunos(self):
        from ListaAlunos import ListaAlunos
        ListaAlunos(self)

    def mostrar_status(self, texto, cor):
        ctk.CTkLabel(
            self.content,
            text=texto,
            text_color=cor,
            font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=10)

    def fechar_tela(self):
        self.destroy()
        if self.master:
            self.master.deiconify()