import os
import getpass
import psycopg2
from werkzeug.security import generate_password_hash

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("Erro: DATABASE_URL não foi encontrada.")
    raise SystemExit

nome = input("Nome do usuário: ").strip()
email = input("E-mail autorizado: ").strip().lower()
senha = getpass.getpass("Senha: ")
confirmacao = getpass.getpass("Confirme a senha: ")

if not nome or not email or not senha:
    print("Preencha todos os campos.")
    raise SystemExit

if senha != confirmacao:
    print("As senhas não coincidem.")
    raise SystemExit

if len(senha) < 8:
    print("A senha deve ter pelo menos 8 caracteres.")
    raise SystemExit

senha_hash = generate_password_hash(senha)

try:
    conexao = psycopg2.connect(DATABASE_URL)

    with conexao:
        with conexao.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO usuarios (nome, email, senha_hash)
                VALUES (%s, %s, %s)
                """,
                (nome, email, senha_hash)
            )

    conexao.close()
    print("Usuário autorizado criado com sucesso!")

except psycopg2.errors.UniqueViolation:
    print("Esse e-mail já está cadastrado.")

except Exception as erro:
    print("Erro ao criar usuário:", erro)