import sqlite3 as connect


def conectar_banco():
    import os
    caminho = os.path.abspath("clientes.db")
    print("Usando banco:", caminho)  # debug
    return connect.connect(caminho)


def criar_tabela():
    print("Chamando criar_tabela()")  # debug
    connection = conectar_banco()
    cursor = connection.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        usuario TEXT UNIQUE,
        senha TEXT,
        pergunta TEXT,
        resposta TEXT,
        tipo TEXT DEFAULT 'usuario'
    )
    """)
    print("Tabela criada ou já existe!")  # debug
    connection.commit()
    connection.close()


# =========================
# USUÁRIOS 
# =========================
def cadastrar_usuario(nome, usuario, senha, pergunta, resposta, tipo):
    connection = None

    try:
        connection = conectar_banco()
        cursor = connection.cursor()

        cursor.execute(
            """INSERT INTO usuarios 
            (nome, usuario, senha, pergunta, resposta, tipo) 
            VALUES (?, ?, ?, ?, ?, ?)""",
            (nome, usuario, senha, pergunta, resposta, tipo)
        )

        connection.commit()
        return True

    except connect.IntegrityError:
        return "existe"

    except Exception as e:
        print("Erro ao cadastrar:", e)
        return False

    finally:
        if connection:
            connection.close()


def verificar_login(usuario, senha):
    connection = conectar_banco()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = ? AND senha = ?",
        (usuario, senha)
    )

    resultado = cursor.fetchone()
    connection.close()

    return resultado


def buscar_pergunta(usuario):
    connection = conectar_banco()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT pergunta FROM usuarios WHERE usuario = ?",
        (usuario,)
    )

    resultado = cursor.fetchone()
    connection.close()

    return resultado


def verificar_resposta(usuario, resposta):
    connection = conectar_banco()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = ? AND resposta = ?",
        (usuario, resposta)
    )

    resultado = cursor.fetchone()
    connection.close()

    return resultado


def atualizar_senha(usuario, nova_senha):
    connection = conectar_banco()
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE usuarios SET senha = ? WHERE usuario = ?",
        (nova_senha, usuario)
    )

    connection.commit()
    connection.close()

    return True


def excluir_usuario(id_usuario):
    connection = conectar_banco()
    cursor = connection.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
    connection.commit()

    if cursor.rowcount > 0:
        print("Usuário deletado com sucesso ✅")
    else:
        print("Usuário não existe ❌")

    connection.close()


def usuario_existe(usuario):
    connection = conectar_banco()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario = ?",
        (usuario,)
    )

    resultado = cursor.fetchone()
    connection.close()

    return resultado

def listar_usuarios():
    conn = conectar_banco()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, nome, usuario, tipo
        FROM usuarios
        ORDER BY nome
    """)

    usuarios = cursor.fetchall()
    conn.close()

    return usuarios