import customtkinter as ctk
from tkinter import messagebox
from banco import conectar_banco, listar_usuarios


class TelaUsuarios(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.title("Usuários do Sistema")
        self.geometry("900x600")
        self.configure(fg_color="#080b12")
        self.grab_set()

        self.container = ctk.CTkFrame(
            self,
            fg_color="#0f172a",
            corner_radius=24,
            border_width=1,
            border_color="#1e293b"
        )
        self.container.pack(expand=True, fill="both", padx=25, pady=25)

        ctk.CTkLabel(
            self.container,
            text="🧑‍💼 Usuários com acesso ao sistema",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w", padx=25, pady=(25, 5))

        ctk.CTkLabel(
            self.container,
            text="Gerencie contas cadastradas no FitSense AI.",
            text_color="#94a3b8"
        ).pack(anchor="w", padx=25, pady=(0, 20))

        self.lista = ctk.CTkScrollableFrame(
            self.container,
            fg_color="transparent"
        )
        self.lista.pack(expand=True, fill="both", padx=20, pady=10)

        self.carregar_usuarios()

    def carregar_usuarios(self):
        for widget in self.lista.winfo_children():
            widget.destroy()

        usuarios = listar_usuarios()

        if not usuarios:
            ctk.CTkLabel(
                self.lista,
                text="Nenhum usuário cadastrado.",
                text_color="#94a3b8"
            ).pack(pady=30)
            return

        for user_id, nome, usuario, tipo in usuarios:
            self.criar_card_usuario(user_id, nome, usuario, tipo)

    def criar_card_usuario(self, user_id, nome, usuario, tipo):
        card = ctk.CTkFrame(
            self.lista,
            fg_color="#111827",
            corner_radius=18,
            border_width=1,
            border_color="#1e293b"
        )
        card.pack(fill="x", padx=5, pady=7)

        info = ctk.CTkFrame(card, fg_color="transparent")
        info.pack(side="left", fill="x", expand=True, padx=18, pady=12)

        ctk.CTkLabel(
            info,
            text=f"👤 {nome}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w")

        ctk.CTkLabel(
            info,
            text=f"Login: {usuario}   |   Tipo: {tipo}",
            text_color="#94a3b8"
        ).pack(anchor="w", pady=(3, 0))

        botoes = ctk.CTkFrame(card, fg_color="transparent")
        botoes.pack(side="right", padx=18, pady=12)

        ctk.CTkButton(
            botoes,
            text="✏️ Editar",
            width=100,
            height=36,
            corner_radius=12,
            fg_color="#2563eb",
            hover_color="#1d4ed8",
            command=lambda: self.abrir_edicao(user_id, nome, usuario, tipo)
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            botoes,
            text="🗑️ Excluir",
            width=100,
            height=36,
            corner_radius=12,
            fg_color="#dc2626",
            hover_color="#991b1b",
            command=lambda: self.excluir_usuario(user_id)
        ).pack(side="left")

    def excluir_usuario(self, user_id):
        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Tem certeza que deseja excluir este usuário?"
        )

        if not confirmar:
            return

        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            cursor.execute("SELECT tipo FROM usuarios WHERE id = ?", (user_id,))
            resultado = cursor.fetchone()

            if resultado and resultado[0] == "admin":
                conn.close()
                messagebox.showwarning(
                    "Bloqueado",
                    "Não é possível excluir um administrador."
                )
                return

            cursor.execute(
                "DELETE FROM usuarios WHERE id = ?",
                (user_id,)
            )

            conn.commit()
            conn.close()

            self.carregar_usuarios()

        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Erro ao excluir usuário:\n{e}"
            )

    def abrir_edicao(self, user_id, nome, usuario, tipo):
        EditarUsuario(
            master=self,
            user_id=user_id,
            nome=nome,
            usuario=usuario,
            tipo=tipo,
            callback=self.carregar_usuarios
        )


class EditarUsuario(ctk.CTkToplevel):
    def __init__(self, master, user_id, nome, usuario, tipo, callback):
        super().__init__(master)

        self.user_id = user_id
        self.callback = callback

        self.title("Editar Usuário")
        self.geometry("520x500")
        self.configure(fg_color="#080b12")
        self.grab_set()
        self.resizable(False, False)

        container = ctk.CTkFrame(
            self,
            fg_color="#0f172a",
            corner_radius=24,
            border_width=1,
            border_color="#1e293b"
        )
        container.pack(expand=True, fill="both", padx=25, pady=25)

        ctk.CTkLabel(
            container,
            text="✏️ Editar Usuário",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#ffffff"
        ).pack(anchor="w", padx=25, pady=(25, 5))

        ctk.CTkLabel(
            container,
            text="Atualize as informações da conta.",
            text_color="#94a3b8"
        ).pack(anchor="w", padx=25, pady=(0, 20))

        self.nome_entry = ctk.CTkEntry(
            container,
            placeholder_text="Nome",
            height=45,
            corner_radius=14,
            fg_color="#111827",
            border_color="#334155"
        )
        self.nome_entry.pack(fill="x", padx=25, pady=8)
        self.nome_entry.insert(0, nome)

        self.usuario_entry = ctk.CTkEntry(
            container,
            placeholder_text="Usuário",
            height=45,
            corner_radius=14,
            fg_color="#111827",
            border_color="#334155"
        )
        self.usuario_entry.pack(fill="x", padx=25, pady=8)
        self.usuario_entry.insert(0, usuario)

        self.tipo_menu = ctk.CTkOptionMenu(
            container,
            values=["usuario", "admin"],
            height=45,
            corner_radius=14,
            fg_color="#111827",
            button_color="#2563eb",
            button_hover_color="#1d4ed8"
        )
        self.tipo_menu.pack(fill="x", padx=25, pady=8)
        self.tipo_menu.set(tipo)

        self.senha_entry = ctk.CTkEntry(
            container,
            placeholder_text="Nova senha (opcional)",
            show="*",
            height=45,
            corner_radius=14,
            fg_color="#111827",
            border_color="#334155"
        )
        self.senha_entry.pack(fill="x", padx=25, pady=8)

        self.status = ctk.CTkLabel(
            container,
            text="",
            font=ctk.CTkFont(size=12)
        )
        self.status.pack(pady=5)

        ctk.CTkButton(
            container,
            text="💾 Salvar alterações",
            height=45,
            corner_radius=14,
            fg_color="#22c55e",
            hover_color="#16a34a",
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.salvar
        ).pack(fill="x", padx=25, pady=(15, 8))

        ctk.CTkButton(
            container,
            text="Cancelar",
            height=42,
            corner_radius=14,
            fg_color="#1e293b",
            hover_color="#334155",
            command=self.destroy
        ).pack(fill="x", padx=25)

    def salvar(self):
        nome = self.nome_entry.get().strip()
        usuario = self.usuario_entry.get().strip()
        tipo = self.tipo_menu.get()
        nova_senha = self.senha_entry.get().strip()

        if not nome or not usuario:
            self.status.configure(
                text="⚠️ Nome e usuário são obrigatórios",
                text_color="#f87171"
            )
            return

        try:
            conn = conectar_banco()
            cursor = conn.cursor()

            if nova_senha:
                cursor.execute("""
                    UPDATE usuarios
                    SET nome = ?, usuario = ?, senha = ?, tipo = ?
                    WHERE id = ?
                """, (nome, usuario, nova_senha, tipo, self.user_id))
            else:
                cursor.execute("""
                    UPDATE usuarios
                    SET nome = ?, usuario = ?, tipo = ?
                    WHERE id = ?
                """, (nome, usuario, tipo, self.user_id))

            conn.commit()
            conn.close()

            self.callback()
            self.destroy()

        except Exception as e:
            self.status.configure(
                text=f"❌ Erro: {e}",
                text_color="#f87171"
            )