import os
import re
from datetime import date
import calendar
import psycopg2
import psycopg2.extras
from create_pdf import criar_pdf
from flask import Flask, flash, redirect, render_template, request, send_file, send_from_directory, url_for

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "troque-esta-chave-em-producao")
DATABASE_URL = os.getenv("DATABASE_URL")


def resumo(erro):
    linhas = str(erro).strip().splitlines()
    return linhas[0] if linhas else type(erro).__name__


def conectar():
    if not DATABASE_URL:
        flash("DATABASE_URL não foi encontrada.", "erro")
        return None
    try:
        return psycopg2.connect(DATABASE_URL, connect_timeout=10)
    except Exception as erro:
        print("Erro ao conectar ao banco:", erro)
        flash(f"Erro ao conectar ao banco de dados: {resumo(erro)}", "erro")
        return None

def validar_cpf(cpf):
    cpf = re.sub(r"\D", "", cpf or "")

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = sum(
        int(cpf[i]) * (10 - i)
        for i in range(9)
    )

    resto = (soma * 10) % 11
    digito1 = 0 if resto == 10 else resto

    if digito1 != int(cpf[9]):
        return False

    # Calcula o segundo dígito verificador
    soma = sum(
        int(cpf[i]) * (11 - i)
        for i in range(10)
    )

    resto = (soma * 10) % 11
    digito2 = 0 if resto == 10 else resto

    if digito2 != int(cpf[10]):
        return False

    return True


def validar_data_nascimento(data_texto):
    try:
        nascimento = date.fromisoformat(data_texto)
    except (ValueError, TypeError):
        return False

    hoje = date.today()

    # Impede datas futuras
    if nascimento > hoje:
        return False

    # Limite de 120 anos
    ano_limite = hoje.year - 120
    mes_limite = hoje.month
    dia_limite = min(
        hoje.day,
        calendar.monthrange(ano_limite, hoje.month)[1]
    )

    data_limite = date(ano_limite, mes_limite, dia_limite)

    if nascimento < data_limite:
        return False

    return True

def consultar(sql, params=()):
    con = conectar()
    if not con:
        return []
    try:
        with con.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(sql, params)
            return cur.fetchall()
    except Exception as erro:
        print("ERRO NA CONSULTA:", erro)
        flash(f"Erro ao consultar o banco de dados: {resumo(erro)}", "erro")
        return []
    finally:
        con.close()


def executar(sql, params=()):
    con = conectar()
    if not con:
        return False

    try:
        with con.cursor() as cur:
            cur.execute(sql, params)

        con.commit()
        return True

    except psycopg2.errors.ForeignKeyViolation:
        con.rollback()
        print("Erro: chave estrangeira inválida.")
        flash(
            "Não foi possível cadastrar! O caso informado não existe. Verifique o ID.",
            "erro"
        )
        return False

    except Exception as erro:
        con.rollback()
        print("Erro no banco:", erro)
        flash(
            f"Erro ao gravar no banco de dados: {resumo(erro)}",
            "erro"
        )
        return False

    finally:
        con.close()


def campo(nome):
    valor = (request.form.get(nome) or "").strip()
    return valor or None


def avisar(ok, texto):
    if ok:
        flash(texto, "ok")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/casos")
def pagina_casos():
    return render_template(
        "mostrar_casos.html",
        casos=consultar("SELECT * FROM casos ORDER BY id")
    )


@app.route("/caso/<int:caso_id>")
def detalhes_caso(caso_id):
    caso = consultar("SELECT * FROM casos WHERE id = %s", (caso_id,))

    if not caso:
        return "Caso não encontrado", 404

    return render_template(
        "detalhes_caso.html",
        caso=caso[0],
        suspeitos=consultar(
            "SELECT * FROM suspeitos WHERE caso_id = %s",
            (caso_id,)
        ),
        evidencias=consultar(
            "SELECT * FROM evidencias WHERE caso_id = %s",
            (caso_id,)
        ),
        testemunhas=consultar(
            "SELECT * FROM testemunhas WHERE caso_id = %s",
            (caso_id,)
        )
    )


@app.route("/investigadores")
def pagina_investigadores():
    return render_template(
        "mostrar_investigadores.html",
        investigadores=consultar("SELECT * FROM investigadores ORDER BY id")
    )


@app.route("/suspeitos")
def pagina_suspeitos():
    return render_template(
        "mostrar_suspeitos.html",
        suspeitos=consultar("SELECT * FROM suspeitos ORDER BY id")
    )


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
        (campo("titulo"), campo("tipo"), campo("descricao"))
    )
    avisar(ok, "Caso registrado com sucesso.")
    return redirect(url_for("pagina_casos"))


@app.route("/salvar-suspeito", methods=["POST"])
def salvar_suspeito():

    nome = campo("nome")
    cpf = campo("cpf")
    nascimento = campo("nascimento")
    endereco = campo("endereco")
    caso_id = campo("caso_id")

    # Verifica o CPF
    if not validar_cpf(cpf):
        flash("CPF inválido! Digite um CPF com dígitos verificadores válidos.", "erro")
        return redirect(url_for("pagina_novo_suspeito"))

    # Verifica a data de nascimento
    if not validar_data_nascimento(nascimento):
        flash(
            "Data de nascimento inválida! Informe uma data entre hoje e 120 anos atrás.",
            "erro"
        )
        return redirect(url_for("pagina_novo_suspeito"))

    # Realiza o cadastro
    ok = executar(
        """
        INSERT INTO suspeitos
        (nome, cpf, data_nascimento, endereco, caso_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            nome,
            re.sub(r"\D", "", cpf),
            nascimento,
            endereco,
            caso_id
        )
    )

    avisar(ok, "Suspeito cadastrado com sucesso.")

    if ok:
        return redirect(url_for("pagina_suspeitos"))

    return redirect(url_for("pagina_novo_suspeito"))


@app.route("/salvar-evidencia", methods=["POST"])
def salvar_evidencia():
    ok = executar(
        "INSERT INTO evidencias (descricao, tipo, local_encontrada, data_coleta, caso_id) VALUES (%s, %s, %s, %s, %s)",
        (
            campo("descricao"),
            campo("tipo"),
            campo("local_encontrada"),
            campo("data_coleta"),
            campo("caso_id")
        )
    )
    avisar(ok, "Evidência adicionada com sucesso.")
    return redirect(url_for("pagina_adicionar_informacoes"))


@app.route("/salvar-testemunha", methods=["POST"])
def salvar_testemunha():
    ok = executar(
        "INSERT INTO testemunhas (nome, telefone, endereco, depoimento, caso_id) VALUES (%s, %s, %s, %s, %s)",
        (
            campo("nome"),
            campo("telefone"),
            campo("endereco"),
            campo("depoimento"),
            campo("caso_id")
        )
    )
    avisar(ok, "Testemunha cadastrada com sucesso.")
    return redirect(url_for("pagina_adicionar_informacoes"))


@app.route("/exportar-pdf-suspeitos")
def exportar_pdf_suspeitos():
    dados = consultar("SELECT nome, cpf FROM suspeitos ORDER BY id")
    lista = [
        f"{x['nome'] or 'Não informado'} (CPF: {x['cpf'] or 'Não informado'})"
        for x in dados
    ]

    return send_file(
        criar_pdf(lista),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="relatorio_suspeitos.pdf"
    )


@app.route("/js/<path:nome>")
def arquivos_js(nome):
    return send_from_directory(
        os.path.join(app.root_path, "js"),
        nome
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)