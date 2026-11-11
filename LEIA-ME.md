# Investigação Policial — Flask no VS Code

## 1. Abrir
VS Code → **Arquivo → Abrir Pasta** → escolha a pasta `investigacao_policial`.
Aceite a sugestão de instalar as extensões recomendadas (Python e Jinja).

## 2. Criar o ambiente e instalar (Terminal → Novo Terminal)

Windows (PowerShell):
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    pip install -r requirements.txt

Se o PowerShell bloquear o Activate, rode uma vez:
    Set-ExecutionPolicy -Scope CurrentUser RemoteSigned

Mac / Linux:
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

Depois: Ctrl+Shift+P → **Python: Select Interpreter** → escolha o que tem `.venv`.

## 3. Rodar
Aperte **F5** (ou o botão verde em "Executar e Depurar", configuração "Rodar site (Flask)").
Abra http://127.0.0.1:5000

Sem depurador, também funciona pelo terminal:
    python app.py

## 4. Banco de dados (PostgreSQL)
Edite o bloco `DB` no topo do `app.py` (host, dbname, user, password).
Sem conexão o site abre, mas as listas aparecem vazias.

## Estrutura
    app.py            rotas do Flask
    templates/        páginas .html
    static/           .css e imagens (img/lupa.webp)
    js/               cadastrar_suspeito.js (servido em /js/...)
