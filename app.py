
import os

from flask import (
    Flask,
    flash,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)

from email import message
from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from flask import Flask, request, jsonify, render_template, redirect, url_for
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash


#67

from dotenv import load_dotenv

try:
    import psycopg2
    import psycopg2.extras
except ImportError:
    psycopg2 = None


load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv(
    "SECRET_KEY",
    "troque-esta-chave-em-producao"
)


app.secret_key = 'uma_chave_super_secreta_e_unica_aqui'

@app.route('/inve', methods=['GET'])
def mostrar_ivestigadores():
    conn = criar_conexao()
    cursor = conn.cursor(cursor_factory=RealDictCursor)


DATABASE_URL = os.getenv("DATABASE_URL")

AVISO_SEM_DRIVER = (
    "O driver do PostgreSQL (psycopg2) não está instalado. "
    "Ative o .venv e rode: pip install -r requirements.txt"
)

AVISO_SEM_DATABASE = (
    "DATABASE_URL não foi encontrada. "
    "Verifique o arquivo .env na raiz do projeto."
)


def resumo(erro):
    linhas = str(erro).strip().splitlines()
    return linhas[0] if linhas else type(erro).__name__


def conectar():
    if psycopg2 is None:
        flash(AVISO_SEM_DRIVER, "erro")
        return None

    if not DATABASE_URL:
        flash(AVISO_SEM_DATABASE, "erro")
        print("ERRO: DATABASE_URL não foi encontrada no arquivo .env.")
        return None

    try:
        return psycopg2.connect(
            DATABASE_URL,
            connect_timeout=10
        )

    except Exception as erro:
        print("Erro ao conectar ao banco:", erro)
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

        with con.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        ) as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    except Exception as erro:
        print("Erro no banco (consulta):", erro)

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

        with con:
            with con.cursor() as cur:
                cur.execute(sql, params)

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
    casos = consultar(
        "SELECT * FROM casos ORDER BY id"
    )

    return render_template(
        "mostrar_casos.html",
        casos=casos
    )


@app.route("/investigadores")
def pagina_investigadores():
    investigadores = consultar(
        "SELECT * FROM investigadores ORDER BY id"
    )

    return render_template(
        "mostrar_investigadores.html",
        investigadores=investigadores
    )


@app.route("/suspeitos")
def pagina_suspeitos():
    suspeitos = consultar(
        "SELECT * FROM suspeitos ORDER BY id"
    )

    return render_template(
        "mostrar_suspeitos.html",
        suspeitos=suspeitos
    )


@app.route("/adicionar-informacoes")
def pagina_adicionar_informacoes():
    return render_template(
        "adicionar_informacoes.html"
    )

@app.route('/inve-s', methods=['POST'])
def cadastrar_testemunhas():
    dados = request.get_json()

    if not dados:
        return jsonify({"erro": "Dados inválidos"}), 400

    print(f"Nova testemunha: {dados}")

    conn = criar_conexao()
    cursor = conn.cursor()

    cursor.execute(
        '''
        INSERT INTO testemunhas(nome, telefone, endereco,depoimento, caso_id) 
        VALUES(%s, %s, %s, %s, %s)
        RETURNING id;
        ''',
        (dados['nome'], dados['telefone'], dados['endereco'],
         dados['depoimento'], dados['caso_id'])
    )

    novo_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()

    return jsonify({
        'message': 'Suspeito cadastrado com sucesso!',
        'id': novo_id,
        'suspeito': dados
    }), 201

@app.route('/nova-testemunha', methods=['GET'])
def pagina_cadastrar_testemunha():
    return render_template('cadastrar_testemunha.html')

@app.route('/cadastrar-testemunha', methods=['POST'])
def salvar_testemunha():
    nome = request.form['nome']
    telefone = request.form['telefone']
    endereco = request.form['endereco']
    depoimento = request.form['depoimento']
    caso_id = request.form['caso_id']

    conn = criar_conexao()
    cursor = conn.cursor()

    try:
        cursor.execute(
            '''
            INSERT INTO testemunhas (nome, telefone, endereco, depoimento, caso_id) 
            VALUES (%s, %s, %s, %s, %s)
            ''',
            (nome, telefone, endereco, depoimento, caso_id)
        )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro ao cadastrar testemunha: {e}")
    finally:
        cursor.close()
        conn.close()

    return redirect(url_for('home'))




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)

        conn = criar_conexao()
        cursor = conn.cursor()

        try:
            cursor.execute(
                "INSERT INTO users (email, password_hash) VALUES (%s, %s)",
                (email, hashed_password)
            )
            conn.commit()
            flash('Conta criada com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            print(f"Erro ao registar: {e}")
            flash('Este e-mail já pode estar registado.', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = criar_conexao()
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute("SELECT id, email, password_hash FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        if user and check_password_hash(user['password_hash'], password):
            session['user_id'] = user['id']
            session['user_email'] = user['email']
            flash('Login efetuado com sucesso!', 'success')
            return redirect(url_for('home'))
        else:
            flash('E-mail ou palavra-passe incorretos.', 'danger')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_email', None)
    flash('Terminou a sessão com sucesso.', 'success')
    return redirect(url_for('login'))





@app.route("/registrar-caso")
def pagina_registrar_caso():
    return render_template(
        "registrar_caso.html"
    )


@app.route("/novo-suspeito")
def pagina_novo_suspeito():
    return render_template(
        "cadastrar_suspeito.html"
    )


@app.route("/nova-evidencia")
def pagina_nova_evidencia():
    return render_template(
        "adicionar_evidencia.html"
    )


@app.route("/nova-testemunha")
def pagina_nova_testemunha():
    return render_template(
        "cadastrar_testemunha.html"
    )


@app.route("/salvar-caso", methods=["POST"])
def salvar_caso():
    ok = executar(
        """
        INSERT INTO casos
        (titulo, tipo_crime, descricao)
        VALUES (%s, %s, %s)
        """,
        (
            campo("titulo"),
            campo("tipo"),
            campo("descricao"),
        ),
    )

    avisar(
        ok,
        "Caso registrado com sucesso."
    )

    return redirect(
        url_for("pagina_casos")
    )


@app.route("/salvar-suspeito", methods=["POST"])
def salvar_suspeito():
    ok = executar(
        """
        INSERT INTO suspeitos
        (nome, cpf, data_nascimento, endereco, caso_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            campo("nome"),
            campo("cpf"),
            campo("nascimento"),
            campo("endereco"),
            campo("caso_id"),
        ),
    )

    avisar(
        ok,
        "Suspeito cadastrado com sucesso."
    )

    return redirect(
        url_for("pagina_suspeitos")
    )


@app.route("/salvar-evidencia", methods=["POST"])
def salvar_evidencia():
    ok = executar(
        """
        INSERT INTO evidencias
        (descricao, tipo, local_encontrada, data_coleta, caso_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            campo("descricao"),
            campo("tipo"),
            campo("local_encontrada"),
            campo("data_coleta"),
            campo("caso_id"),
        ),
    )

    avisar(
        ok,
        "Evidência adicionada com sucesso."
    )

    return redirect(
        url_for("pagina_adicionar_informacoes")
    )


@app.route("/salvar-testemunha", methods=["POST"])
def salvar_testemunha():
    ok = executar(
        """
        INSERT INTO testemunhas
        (nome, telefone, endereco, depoimento, caso_id)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (
            campo("nome"),
            campo("telefone"),
            campo("endereco"),
            campo("depoimento"),
            campo("caso_id"),
        ),
    )

    avisar(
        ok,
        "Testemunha cadastrada com sucesso."
    )

    return redirect(
        url_for("pagina_adicionar_informacoes")
    )


@app.route("/js/<path:nome>")
def arquivos_js(nome):
    return send_from_directory(
        os.path.join(app.root_path, "js"),
        nome
    )


if __name__ == "__main__":
    print("=" * 60)
    print("SISTEMA DE INVESTIGAÇÃO POLICIAL")
    print("=" * 60)

    if DATABASE_URL:
        print("✓ DATABASE_URL encontrada.")
        print("✓ Banco configurado para utilizar o Neon.")
    else:
        print("✗ DATABASE_URL NÃO encontrada.")
        print("  Verifique o arquivo .env.")

    print("=" * 60)

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
