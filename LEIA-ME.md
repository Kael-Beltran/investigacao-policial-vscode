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

## 4. Banco de dados (Neon/PostgreSQL)
O app usa a variável de ambiente `DATABASE_URL`. No Neon, copie a connection string
(de preferência a pooled connection string) e configure-a como `DATABASE_URL`.
O Neon fornece uma conexão TLS; mantenha `sslmode=require` na URL.

Antes do primeiro uso, execute o conteúdo de `schema.sql` no SQL Editor do Neon.
Configure também `SECRET_KEY` como variável de ambiente, usando um valor aleatório
forte; não publique essas variáveis no Git.

## 5. Deploy no Vercel
Importe o repositório no Vercel e configure `DATABASE_URL` e `SECRET_KEY` nas
Environment Variables do projeto para os ambientes desejados (Production,
Preview e/ou Development). Faça um novo deploy após salvar as variáveis.

O arquivo `.env` é apenas para desenvolvimento local e não deve ser enviado ao Git.

## Estrutura
    app.py            rotas do Flask
    templates/        páginas .html
    static/           .css e imagens (img/lupa.webp)
    js/               cadastrar_suspeito.js (servido em /js/...)
