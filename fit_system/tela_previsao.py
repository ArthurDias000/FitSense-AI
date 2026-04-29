import customtkinter as ctk
from ia_modelo import prever_cancelamento


class TelaPrevisao(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("FitSense AI - Previsão")
        self.geometry("720x820")
        self.configure(fg_color="#080b12")

        self.grab_set()
        self.resizable(False, False)

        # =========================
        # CONTAINER PRINCIPAL
        # =========================
        self.container = ctk.CTkFrame(
            self,
            corner_radius=28,
            fg_color="#0f172a",
            border_width=1,
            border_color="#1e293b"
        )
        self.container.pack(expand=True, fill="both", padx=28, pady=28)

        # =========================
        # HEADER
        # =========================
        self.header = ctk.CTkFrame(self.container, fg_color="transparent")
        self.header.pack(fill="x", padx=28, pady=(24, 12))

        ctk.CTkLabel(
            self.header,
            text="🔮 Previsão Inteligente",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w")

        ctk.CTkLabel(
            self.header,
            text="Analise o risco de cancelamento de um cliente com base em comportamento e perfil.",
            text_color="#94a3b8",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", pady=(4, 0))

        # =========================
        # FORMULÁRIO
        # =========================
        self.form_card = ctk.CTkFrame(
            self.container,
            corner_radius=24,
            fg_color="#111827",
            border_width=1,
            border_color="#1e293b"
        )
        self.form_card.pack(fill="x", padx=28, pady=15)

        self.form = ctk.CTkFrame(self.form_card, fg_color="transparent")
        self.form.pack(fill="x", padx=22, pady=22)

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

        label("Nome do Cliente", 0, 0)
        self.nome = entry("Ex: João da Silva", 1, 0, colspan=2)

        self.atraso_var = ctk.BooleanVar()
        self.personal_var = ctk.BooleanVar()

        self.checks = ctk.CTkFrame(self.form, fg_color="transparent")
        self.checks.grid(row=2, column=0, columnspan=2, sticky="ew", pady=8)

        ctk.CTkCheckBox(
            self.checks,
            text="Pagamento atrasado",
            variable=self.atraso_var,
            fg_color="#ef4444",
            hover_color="#dc2626",
            text_color="#e5e7eb"
        ).pack(side="left", padx=8)

        ctk.CTkCheckBox(
            self.checks,
            text="Possui personal trainer",
            variable=self.personal_var,
            fg_color="#22c55e",
            hover_color="#16a34a",
            text_color="#e5e7eb"
        ).pack(side="left", padx=20)

        label("Satisfação", 3, 0)
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
        self.satisfacao.grid(row=4, column=0, padx=8, pady=(0, 8), sticky="ew")

        label("Frequência semanal", 3, 1)
        self.freq = entry("Ex: 3", 4, 1)

        label("Tempo de plano (meses)", 5, 0)
        self.tempo = entry("Ex: 6", 6, 0)

        label("Idade", 5, 1)
        self.idade = entry("Ex: 25", 6, 1)

        label("Valor do plano", 7, 0)
        self.valor = entry("Ex: 120", 8, 0, colspan=2)

        # =========================
        # BOTÃO
        # =========================
        self.btn = ctk.CTkButton(
            self.container,
            text="🔍 Calcular risco de cancelamento",
            height=52,
            corner_radius=16,
            fg_color="#38bdf8",
            hover_color="#0284c7",
            text_color="#020617",
            font=ctk.CTkFont(size=15, weight="bold"),
            command=self.prever
        )
        self.btn.pack(pady=(8, 18), padx=28, fill="x")

        # =========================
        # RESULTADO
        # =========================
        self.resultado_frame = ctk.CTkFrame(
            self.container,
            corner_radius=24,
            fg_color="#111827",
            border_width=1,
            border_color="#1e293b"
        )
        self.resultado_frame.pack(fill="x", padx=28, pady=(0, 22))

        self.resultado_titulo = ctk.CTkLabel(
            self.resultado_frame,
            text="Resultado",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color="#ffffff"
        )
        self.resultado_titulo.pack(anchor="w", padx=22, pady=(18, 4))

        self.resultado = ctk.CTkLabel(
            self.resultado_frame,
            text="Preencha os dados e clique em calcular.",
            font=ctk.CTkFont(size=14),
            text_color="#94a3b8",
            justify="left",
            wraplength=600
        )
        self.resultado.pack(anchor="w", padx=22, pady=(0, 18))

    def prever(self):
        try:
            resultado = prever_cancelamento(
                self.atraso_var.get(),
                self.satisfacao.get(),
                self.personal_var.get(),
                int(self.freq.get()),
                int(self.tempo.get()),
                int(self.idade.get()),
                float(self.valor.get())
            )

            risco = resultado["risco"]
            prob = resultado["probabilidade"]
            detalhes = "\n".join(resultado["detalhes"])

            if risco == "ALTO":
                cor = "#ef4444"
                msg = "⚠️ ALTO RISCO"
            elif risco == "MÉDIO":
                cor = "#f59e0b"
                msg = "⚠️ RISCO MÉDIO"
            else:
                cor = "#22c55e"
                msg = "✔ BAIXO RISCO"

            cliente = self.nome.get().strip()
            titulo = f"{cliente} — {msg}" if cliente else msg

            self.resultado_frame.configure(border_color=cor)
            self.resultado_titulo.configure(text=titulo, text_color=cor)

            texto = f"Probabilidade de cancelamento: {prob}%"

            if detalhes:
                texto += f"\n\nPrincipais fatores:\n{detalhes}"
            else:
                texto += "\n\nNenhum fator crítico identificado."

            self.resultado.configure(
                text=texto,
                text_color="#e5e7eb"
            )

        except Exception:
            self.resultado_frame.configure(border_color="#ef4444")
            self.resultado_titulo.configure(
                text="⚠️ Dados incompletos ou inválidos",
                text_color="#ef4444"
            )
            self.resultado.configure(
                text="Preencha todos os campos numéricos corretamente antes de calcular.",
                text_color="#fca5a5"
            )