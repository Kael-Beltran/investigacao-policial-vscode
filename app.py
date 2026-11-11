import os
from urllib.parse import urlparse
import pg8000.native

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

# Tenta carregar o dotenv para desenvolvimento local
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "troque-esta-chave-em-producao"
)

DATABASE_URL = os.getenv("DATABASE_URL")

AVISO_SEM_DATABASE = (
    "DATABASE_URL não foi encontrada. "
    "Verifique o arquivo .env na raiz do projeto ou no painel da Vercel."
)


def resumo(erro):
    linhas = str(erro).strip().splitlines()
    return linhas[0] if linhas else type(erro).__name__


def conectar():
    if not DATABASE_URL:
        flash(AVISO_SEM_DATABASE, "erro")
        print("ERRO: DATABASE_URL não foi encontrada.")
        return None

    try:
        url = urlparse(DATABASE_URL)
        conexao = pg8000.native.Connection(
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port or 5432,
            database=url.path.lstrip("/"),
            ssl_context=True
        )
        return conexao
    except Exception as erro:
        print("ERRO DE CONEXÃO COM O NEON:", erro)
        flash(
            f"Erro ao conectar ao banco de dados: {resumo(erro)}",
            "erro"
        )
        return None


def consultar(sql, params=()):
    con = None
    try:
        con = conectar()
        if con is None:
            return []

        # Substitui a sintaxe de placeholder do psycopg2 (%s) para pg8000 (:1, :2, etc)
        sql_formatado = sql
        for i in range(len(params), 0, -1):
            sql_formatado = sql_formatado.replace("%s", f":{i}", 1)

        resultado_bruto = con.run(sql_formatado, *params)
        
        # Converte as colunas para um dicionário (estilo RealDictCursor)
        colunas = [col["name"] for col in con.columns]
        resultado = [dict(zip(colunas, linha)) for linha in resultado_bruto]

        return resultado

    except Exception as erro:
        print("❌ ERRO NA CONSULTA:", repr(erro))
        flash(
            f"Erro ao consultar o banco de dados: {resumo(erro)}",
            "erro"
        )
        return []
    finally:
        if con:
            con.close()


def executar(sql, params=()):
    con = None
    try:
        con = conectar()
        if con is None:
            return False

        sql_formatado = sql
        for i in range(len(params), 0, -1):
            sql_formatado = sql_formatado.replace("%s", f":{i}", 1)

        con.run(sql_formatado, *params)
        return True

    except Exception as erro:
        print("Erro no banco (gravação):", erro)
        flash(
            f"Erro ao gravar no banco de dados: {resumo(erro)}",
            "erro"
        )
        return False
    finally:
        if con:
            con.close()


def campo(nome):
    valor = (request.form.get(nome) or "").strip()
    return valor or None


def avisar(ok, texto_ok):
    if ok:
        flash(texto_ok, "ok")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/casos")
def pagina_casos():
    casos = consultar("SELECT * FROM casos ORDER BY id")
    return render_template("mostrar_casos.html", casos=casos)


@app.route("/investigadores")
def pagina_investigadores():
    investigadores = consultar("SELECT * FROM investigadores ORDER BY id")
    return render_template("mostrar_investigadores.html", investigadores=investigadores)


@app.route("/suspeitos")
def pagina_suspeitos():
    suspeitos = consultar("SELECT * FROM suspeitos ORDER BY id")
    return render_template("mostrar_suspeitos.html", suspeitos=suspeitos)


@app.route("/adicionar-informacoes")
def pagina_adicionar_informacoes():
    return render_template("adicionar_informacoes.html")


@app.route("/registrar-caso")
def pagina_registrar_caso():
    return render_template("registrar_caso.html")


@app.route("/novo-suspeito")
def pagina_novo_suspeito():
    return render_template("cadastrar_suspeito.html")


@app.route("/nova-evidencia")
def pagina_nova_evidencia():
    return render_template("adicionar_evidencia.html")


@app.route("/nova-testemunha")
def pagina_nova_testemunha():
    return render_template("cadastrar_testemunha.html")


@app.route("/salvar-caso", methods=["POST"])
def salvar_caso():
    ok = executar(
        "INSERT INTO casos (titulo, tipo_crime, descricao) VALUES (%s, %s, %s)",
        (campo("titulo"), campo("tipo"), campo("descricao")),
    )
    avisar(ok, "Caso registrado com sucesso.")
    return redirect(url_for("pagina_casos"))


@app.route("/salvar-suspeito", methods=["POST"])
def salvar_suspeito():
    ok = executar(
        "INSERT INTO suspeitos (nome, cpf, data_nascimento, endereco, caso_id) VALUES (%s, %s, %s, %s, %s)",
        (campo("nome"), campo("cpf"), campo("nascimento"), campo("endereco"), campo("caso_id")),
    )
    avisar(ok, "Suspeito cadastrado com sucesso.")
    return redirect(url_for("pagina_suspeitos"))


@app.route("/salvar-evidencia", methods=["POST"])
def salvar_evidencia():
    ok = executar(
        "INSERT INTO evidencias (descricao, tipo, local_encontrada, data_coleta, caso_id) VALUES (%s, %s, %s, %s, %s)",
        (campo("descricao"), campo("tipo"), campo("local_encontrada"), campo("data_coleta"), campo("caso_id")),
    )
    avisar(ok, "Evidência adicionada com sucesso.")
    return redirect(url_for("pagina_adicionar_informacoes"))


@app.route("/salvar-testemunha", methods=["POST"])
def salvar_testemunha():
    ok = executar(
        "INSERT INTO testemunhas (nome, telefone, endereco, depoimento, caso_id) VALUES (%s, %s, %s, %s, %s)",
        (campo("nome"), campo("telefone"), campo("endereco"), campo("depoimento"), campo("caso_id")),
    )
    avisar(ok, "Testemunha cadastrada com sucesso.")
    return redirect(url_for("pagina_adicionar_informacoes"))


@app.route("/js/<path:nome>")
def arquivos_js(nome):
    return send_from_directory(os.path.join(app.root_path, "js"), nome)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)