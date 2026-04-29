import customtkinter as ctk
from banco import conectar_banco
import pandas as pd
from tkinter import filedialog, messagebox


class CadastrarAluno(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("FitSense AI - Cadastro de Aluno")
        self.geometry("760x900")
        self.configure(fg_color="#080b12")
        self.grab_set()
        self.resizable(False, False)

        self.container = ctk.CTkFrame(
            self,
            corner_radius=28,
            fg_color="#0f172a",
            border_width=1,
            border_color="#1e293b"
        )
        self.container.pack(expand=True, fill="both", padx=28, pady=28)

        # HEADER
        ctk.CTkLabel(
            self.container,
            text="➕ Cadastrar Aluno",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w", padx=32, pady=(28, 4))

        ctk.CTkLabel(
            self.container,
            text="Registre os dados do aluno para análise e acompanhamento inteligente.",
            text_color="#94a3b8",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=32, pady=(0, 20))

        # FORM CARD
        self.form_card = ctk.CTkFrame(
            self.container,
            corner_radius=24,
            fg_color="#111827",
            border_width=1,
            border_color="#1e293b"
        )
        self.form_card.pack(fill="x", padx=32, pady=(0, 18))

        self.form = ctk.CTkFrame(self.form_card, fg_color="transparent")
        self.form.pack(fill="x", padx=24, pady=24)

        for i in range(2):
            self.form.grid_columnconfigure(i, weight=1)

        def label(texto, row, col):
            ctk.CTkLabel(
                self.form,
                text=texto,
                text_color="#cbd5e1",
                font=ctk.CTkFont(size=13, weight="bold")
            ).grid(row=row, column=col, sticky="w", padx=8, pady=(8, 3))

        def entry(placeholder, row, col, colspan=1):
            campo = ctk.CTkEntry(
                self.form,
                placeholder_text=placeholder,
                height=44,
                corner_radius=14,
                fg_color="#0f172a",
                border_color="#334155",
                border_width=1
            )
            campo.grid(row=row, column=col, columnspan=colspan, padx=8, pady=(0, 8), sticky="ew")
            return campo

        label("Nome", 0, 0)
        self.nome = entry("Ex: João da Silva", 1, 0, colspan=2)

        label("Idade", 2, 0)
        self.idade = entry("Ex: 28", 3, 0)

        label("Telefone", 2, 1)
        self.telefone = entry("Ex: 11999999999", 3, 1)

        label("Tempo na academia", 4, 0)
        self.tempo = entry("Meses. Ex: 12", 5, 0)

        label("Frequência semanal", 4, 1)
        self.freq = entry("Ex: 3", 5, 1)

        label("Valor do plano", 6, 0)
        self.valor = entry("Ex: 120.00", 7, 0)

        label("Satisfação", 6, 1)
        self.satisfacao = ctk.CTkOptionMenu(
            self.form,
            values=["boa", "media", "ruim"],
            height=44,
            corner_radius=14,
            fg_color="#0f172a",
            button_color="#38bdf8",
            button_hover_color="#0284c7",
            dropdown_fg_color="#111827",
            dropdown_hover_color="#1e293b"
        )
        self.satisfacao.grid(row=7, column=1, padx=8, pady=(0, 8), sticky="ew")

        self.checks = ctk.CTkFrame(self.form, fg_color="transparent")
        self.checks.grid(row=8, column=0, columnspan=2, sticky="w", pady=(10, 4))

        self.personal = ctk.BooleanVar()
        ctk.CTkCheckBox(
            self.checks,
            text="Possui personal",
            variable=self.personal,
            fg_color="#22c55e",
            hover_color="#16a34a",
            text_color="#e5e7eb"
        ).pack(side="left", padx=8)

        self.atraso = ctk.BooleanVar()
        ctk.CTkCheckBox(
            self.checks,
            text="Pagamento atrasado",
            variable=self.atraso,
            fg_color="#ef4444",
            hover_color="#dc2626",
            text_color="#e5e7eb"
        ).pack(side="left", padx=24)

        # STATUS
        self.status = ctk.CTkLabel(
            self.container,
            text="",
            font=ctk.CTkFont(size=13, weight="bold"),
            wraplength=620
        )
        self.status.pack(padx=32, pady=(0, 8))

        # BUTTONS
        self.btn_salvar = ctk.CTkButton(
            self.container,
            text="💾 Salvar Aluno",
            height=50,
            corner_radius=16,
            fg_color="#38bdf8",
            hover_color="#0284c7",
            text_color="#020617",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.salvar
        )
        self.btn_salvar.pack(fill="x", padx=32, pady=(5, 14))

        # IMPORT CARD
        self.import_card = ctk.CTkFrame(
            self.container,
            corner_radius=24,
            fg_color="#111827",
            border_width=1,
            border_color="#1e293b"
        )
        self.import_card.pack(fill="x", padx=32, pady=(0, 22))

        ctk.CTkLabel(
            self.import_card,
            text="📂 Importação em massa",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w", padx=22, pady=(18, 4))

        ctk.CTkLabel(
            self.import_card,
            text=(
                "Use o modelo padrão com as colunas:\n"
                "nome, idade, telefone, tempo, freq, valor, satisfacao, personal, atraso"
            ),
            text_color="#94a3b8",
            font=ctk.CTkFont(size=13),
            justify="left",
            wraplength=620
        ).pack(anchor="w", padx=22, pady=(0, 14))

        self.import_buttons = ctk.CTkFrame(self.import_card, fg_color="transparent")
        self.import_buttons.pack(fill="x", padx=22, pady=(0, 18))

        ctk.CTkButton(
            self.import_buttons,
            text="⬇️ Baixar Modelo Excel",
            height=44,
            corner_radius=14,
            fg_color="#1e293b",
            hover_color="#334155",
            command=self.baixar_modelo_excel
        ).pack(side="left", expand=True, fill="x", padx=(0, 8))

        ctk.CTkButton(
            self.import_buttons,
            text="📥 Importar Planilha",
            height=44,
            corner_radius=14,
            fg_color="#22c55e",
            hover_color="#16a34a",
            command=self.importar_planilha
        ).pack(side="left", expand=True, fill="x", padx=(8, 0))

    def salvar(self):
        try:
            connection = conectar_banco()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    idade INTEGER,
                    telefone TEXT,
                    tempo INTEGER,
                    freq INTEGER,
                    valor REAL,
                    satisfacao TEXT,
                    personal BOOLEAN,
                    atraso BOOLEAN
                )
            """)

            cursor.execute("""
                INSERT INTO alunos 
                (nome, idade, telefone, tempo, freq, valor, satisfacao, personal, atraso)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                self.nome.get(),
                int(self.idade.get()),
                self.telefone.get(),
                int(self.tempo.get()),
                int(self.freq.get()),
                float(self.valor.get()),
                self.satisfacao.get(),
                self.personal.get(),
                self.atraso.get()
            ))

            connection.commit()
            connection.close()

            self.status.configure(
                text="✅ Aluno cadastrado com sucesso!",
                text_color="#22c55e"
            )
            self.limpar_campos()

        except Exception as e:
            self.status.configure(
                text=f"❌ Erro: {e}",
                text_color="#ef4444"
            )

    def limpar_campos(self):
        self.nome.delete(0, "end")
        self.idade.delete(0, "end")
        self.telefone.delete(0, "end")
        self.tempo.delete(0, "end")
        self.freq.delete(0, "end")
        self.valor.delete(0, "end")
        self.satisfacao.set("boa")
        self.personal.set(False)
        self.atraso.set(False)

    def baixar_modelo_excel(self):
        colunas = [
            "nome", "idade", "telefone", "tempo", "freq",
            "valor", "satisfacao", "personal", "atraso"
        ]

        exemplo = [{
            "nome": "João da Silva",
            "idade": 28,
            "telefone": "11999999999",
            "tempo": 12,
            "freq": 3,
            "valor": 120.0,
            "satisfacao": "boa",
            "personal": True,
            "atraso": False
        }]

        df = pd.DataFrame(exemplo, columns=colunas)

        caminho = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Salvar modelo de alunos"
        )

        if caminho:
            df.to_excel(caminho, index=False)
            messagebox.showinfo("Modelo salvo", "Modelo de Excel salvo com sucesso!")

    def importar_planilha(self):
        caminho = filedialog.askopenfilename(
            title="Selecione a planilha Excel",
            filetypes=[("Excel files", "*.xlsx")]
        )

        if not caminho:
            return

        try:
            df = pd.read_excel(caminho)

            colunas_esperadas = [
                "nome", "idade", "telefone", "tempo", "freq",
                "valor", "satisfacao", "personal", "atraso"
            ]

            if list(df.columns) != colunas_esperadas:
                messagebox.showerror(
                    "Erro",
                    "❌ Modelo de planilha inválido!\nBaixe o modelo correto."
                )
                return

            connection = conectar_banco()
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS alunos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    nome TEXT,
                    idade INTEGER,
                    telefone TEXT,
                    tempo INTEGER,
                    freq INTEGER,
                    valor REAL,
                    satisfacao TEXT,
                    personal BOOLEAN,
                    atraso BOOLEAN
                )
            """)

            for _, row in df.iterrows():
                cursor.execute("""
                    INSERT INTO alunos 
                    (nome, idade, telefone, tempo, freq, valor, satisfacao, personal, atraso)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    row["nome"],
                    int(row["idade"]),
                    str(row["telefone"]),
                    int(row["tempo"]),
                    int(row["freq"]),
                    float(row["valor"]),
                    row["satisfacao"],
                    bool(row["personal"]),
                    bool(row["atraso"])
                ))

            connection.commit()
            connection.close()

            messagebox.showinfo(
                "Importação concluída",
                "✅ Alunos importados com sucesso!"
            )

        except Exception as e:
            messagebox.showerror(
                "Erro ao importar",
                f"Erro ao importar: {e}"
            )