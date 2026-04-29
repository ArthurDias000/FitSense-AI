import customtkinter as ctk
from banco import conectar_banco
from tkinter import messagebox


class ListaAlunos(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("FitSense AI - Lista de Alunos")
        self.geometry("1100x650")
        self.configure(fg_color="#080b12")
        self.grab_set()

        self.container = ctk.CTkFrame(
            self,
            fg_color="#0f172a",
            corner_radius=26,
            border_width=1,
            border_color="#1e293b"
        )
        self.container.pack(expand=True, fill="both", padx=28, pady=28)

        ctk.CTkLabel(
            self.container,
            text="📋 Alunos Cadastrados",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w", padx=28, pady=(24, 4))

        ctk.CTkLabel(
            self.container,
            text="Gerencie os alunos cadastrados, edite informações ou remova registros.",
            text_color="#94a3b8",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=28, pady=(0, 18))

        self.lista_frame = ctk.CTkScrollableFrame(
            self.container,
            fg_color="transparent"
        )
        self.lista_frame.pack(expand=True, fill="both", padx=20, pady=(0, 20))

        self.carregar_alunos()

    def limpar_lista(self):
        for widget in self.lista_frame.winfo_children():
            widget.destroy()

    def carregar_alunos(self):
        self.limpar_lista()

        connection = conectar_banco()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, nome, idade, telefone, tempo, freq, valor, satisfacao, personal, atraso
            FROM alunos
        """)

        alunos = cursor.fetchall()
        connection.close()

        if not alunos:
            ctk.CTkLabel(
                self.lista_frame,
                text="Nenhum aluno cadastrado 😢",
                text_color="#94a3b8",
                font=ctk.CTkFont(size=16)
            ).pack(pady=40)
            return

        for aluno in alunos:
            self.criar_card_aluno(aluno)

    def criar_card_aluno(self, aluno):
        aluno_id, nome, idade, telefone, tempo, freq, valor, satisfacao, personal, atraso = aluno

        card = ctk.CTkFrame(
            self.lista_frame,
            fg_color="#111827",
            corner_radius=22,
            border_width=1,
            border_color="#1e293b"
        )
        card.pack(fill="x", padx=8, pady=8)

        top = ctk.CTkFrame(card, fg_color="transparent")
        top.pack(fill="x", padx=18, pady=(14, 4))

        ctk.CTkLabel(
            top,
            text=f"👤 {nome}",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        ).pack(side="left")

        valor_formatado = f"R$ {float(valor):.2f}".replace(".", ",")

        ctk.CTkLabel(
            top,
            text=valor_formatado,
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#38bdf8"
        ).pack(side="right")

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(fill="x", padx=18, pady=(4, 12))

        status_pagamento = "Atrasado" if atraso else "Em dia"
        status_personal = "Sim" if personal else "Não"

        detalhes = (
            f"🎂 {idade} anos   |   📞 {telefone}   |   "
            f"📅 {freq}x/semana   |   ⏳ {tempo} meses   |   "
            f"😊 {satisfacao}   |   🏋️ Personal: {status_personal}   |   "
            f"💳 Pagamento: {status_pagamento}"
        )

        ctk.CTkLabel(
            info,
            text=detalhes,
            text_color="#94a3b8",
            font=ctk.CTkFont(size=13),
            anchor="w"
        ).pack(side="left", fill="x", expand=True)

        botoes = ctk.CTkFrame(card, fg_color="transparent")
        botoes.pack(fill="x", padx=18, pady=(0, 14))

        ctk.CTkButton(
            botoes,
            text="✏️ Editar",
            width=110,
            height=36,
            corner_radius=12,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=lambda: self.abrir_edicao(aluno)
        ).pack(side="right", padx=(8, 0))

        ctk.CTkButton(
            botoes,
            text="🗑️ Excluir",
            width=110,
            height=36,
            corner_radius=12,
            fg_color="#dc2626",
            hover_color="#991b1b",
            command=lambda: self.excluir_aluno(aluno_id)
        ).pack(side="right")

    def excluir_aluno(self, aluno_id):
        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Tem certeza que deseja excluir este aluno?"
        )

        if not confirmar:
            return

        connection = conectar_banco()
        cursor = connection.cursor()

        cursor.execute("DELETE FROM alunos WHERE id = ?", (aluno_id,))

        connection.commit()
        connection.close()

        self.carregar_alunos()

    def abrir_edicao(self, aluno):
        EditarAluno(self, aluno, self.carregar_alunos)


class EditarAluno(ctk.CTkToplevel):
    def __init__(self, master, aluno, callback):
        super().__init__(master)

        self.callback = callback

        (
            self.aluno_id,
            nome,
            idade,
            telefone,
            tempo,
            freq,
            valor,
            satisfacao,
            personal,
            atraso
        ) = aluno

        self.title("Editar Aluno")
        self.geometry("620x720")
        self.configure(fg_color="#080b12")
        self.grab_set()
        self.resizable(False, False)

        self.container = ctk.CTkFrame(
            self,
            fg_color="#0f172a",
            corner_radius=26,
            border_width=1,
            border_color="#1e293b"
        )
        self.container.pack(expand=True, fill="both", padx=28, pady=28)

        ctk.CTkLabel(
            self.container,
            text="✏️ Editar Aluno",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w", padx=28, pady=(24, 4))

        ctk.CTkLabel(
            self.container,
            text="Atualize os dados do aluno selecionado.",
            text_color="#94a3b8"
        ).pack(anchor="w", padx=28, pady=(0, 20))

        self.form = ctk.CTkFrame(self.container, fg_color="transparent")
        self.form.pack(fill="x", padx=28)

        for i in range(2):
            self.form.grid_columnconfigure(i, weight=1)

        def criar_entry(label, valor_inicial, row, col, colspan=1):
            ctk.CTkLabel(
                self.form,
                text=label,
                text_color="#cbd5e1",
                font=ctk.CTkFont(size=13, weight="bold")
            ).grid(row=row, column=col, sticky="w", padx=8, pady=(8, 3))

            entry = ctk.CTkEntry(
                self.form,
                height=44,
                corner_radius=14,
                fg_color="#111827",
                border_color="#334155"
            )
            entry.grid(row=row + 1, column=col, columnspan=colspan, padx=8, pady=(0, 8), sticky="ew")
            entry.insert(0, str(valor_inicial))
            return entry

        self.nome = criar_entry("Nome", nome, 0, 0, 2)
        self.idade = criar_entry("Idade", idade, 2, 0)
        self.telefone = criar_entry("Telefone", telefone, 2, 1)
        self.tempo = criar_entry("Tempo na academia", tempo, 4, 0)
        self.freq = criar_entry("Frequência semanal", freq, 4, 1)
        self.valor = criar_entry("Valor do plano", valor, 6, 0)

        ctk.CTkLabel(
            self.form,
            text="Satisfação",
            text_color="#cbd5e1",
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=6, column=1, sticky="w", padx=8, pady=(8, 3))

        self.satisfacao = ctk.CTkOptionMenu(
            self.form,
            values=["boa", "media", "ruim"],
            height=44,
            corner_radius=14,
            fg_color="#111827",
            button_color="#38bdf8",
            button_hover_color="#0284c7"
        )
        self.satisfacao.grid(row=7, column=1, padx=8, pady=(0, 8), sticky="ew")
        self.satisfacao.set(satisfacao)

        self.personal = ctk.BooleanVar(value=bool(personal))
        self.atraso = ctk.BooleanVar(value=bool(atraso))

        checks = ctk.CTkFrame(self.form, fg_color="transparent")
        checks.grid(row=8, column=0, columnspan=2, sticky="w", pady=12)

        ctk.CTkCheckBox(
            checks,
            text="Possui personal",
            variable=self.personal,
            fg_color="#22c55e",
            hover_color="#16a34a"
        ).pack(side="left", padx=8)

        ctk.CTkCheckBox(
            checks,
            text="Pagamento atrasado",
            variable=self.atraso,
            fg_color="#ef4444",
            hover_color="#dc2626"
        ).pack(side="left", padx=24)

        self.status = ctk.CTkLabel(
            self.container,
            text="",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.status.pack(pady=(8, 0))

        ctk.CTkButton(
            self.container,
            text="💾 Salvar Alterações",
            height=50,
            corner_radius=16,
            fg_color="#38bdf8",
            hover_color="#0284c7",
            text_color="#020617",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.salvar_edicao
        ).pack(fill="x", padx=28, pady=(16, 10))

        ctk.CTkButton(
            self.container,
            text="Cancelar",
            height=44,
            corner_radius=14,
            fg_color="#1e293b",
            hover_color="#334155",
            command=self.destroy
        ).pack(fill="x", padx=28)

    def salvar_edicao(self):
        try:
            connection = conectar_banco()
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE alunos
                SET nome = ?,
                    idade = ?,
                    telefone = ?,
                    tempo = ?,
                    freq = ?,
                    valor = ?,
                    satisfacao = ?,
                    personal = ?,
                    atraso = ?
                WHERE id = ?
            """, (
                self.nome.get(),
                int(self.idade.get()),
                self.telefone.get(),
                int(self.tempo.get()),
                int(self.freq.get()),
                float(self.valor.get()),
                self.satisfacao.get(),
                self.personal.get(),
                self.atraso.get(),
                self.aluno_id
            ))

            connection.commit()
            connection.close()

            self.callback()
            self.destroy()

        except Exception as e:
            self.status.configure(
                text=f"Erro ao salvar: {e}",
                text_color="#ef4444"
            )