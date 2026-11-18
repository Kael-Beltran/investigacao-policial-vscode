# 🔎 Projeto de Investigação Policial

Sistema web desenvolvido para **gerenciamento e organização de investigações policiais**, permitindo o cadastro e a consulta de informações relacionadas aos casos.

## 🌐 Acesse o projeto

(https://investigacao-policial-vscode.vercel.app/)

---

## 📌 Sobre o projeto

O **Projeto de Investigação Policial** foi desenvolvido com o objetivo de criar um sistema para auxiliar no gerenciamento de investigações, centralizando informações importantes de cada caso em um único ambiente.

O sistema permite registrar e consultar dados como:

- 📁 Casos policiais
- 👤 Suspeitos
- 🧑‍💼 Investigadores
- 🧪 Evidências
- 👥 Testemunhas
- 📄 Relatórios

Ao selecionar um caso, é possível visualizar as informações relacionadas a ele, facilitando a organização e consulta dos dados da investigação.

---

## ⚙️ Funcionalidades

- Cadastro de novos casos
- Cadastro de suspeitos
- Cadastro de evidências
- Cadastro de testemunhas
- Consulta de casos registrados
- Consulta de suspeitos
- Visualização dos detalhes de um caso
- Organização das informações por caso
- Geração de relatório em PDF
- Armazenamento dos dados em banco de dados PostgreSQL

---

## 🛠️ Tecnologias utilizadas

### Front-end
- HTML5
- CSS3
- JavaScript

### Back-end
- Python
- Flask

### Banco de dados
- PostgreSQL
- Neon

### Outras ferramentas
- Git
- GitHub
- Vercel
- python-dotenv
- psycopg2
- FPDF2

---

## 📂 Estrutura do projeto

```text
investigacao-policial-vscode/
│
├── app.py
├── create_pdf.py
├── requirements.txt
├── README.md
│
├── static/
│   ├── style.css
│   ├── site.css
│   └── outros arquivos CSS
│
├── templates/
│   ├── index.html
│   ├── mostrar_casos.html
│   ├── detalhes_caso.html
│   ├── mostrar_suspeitos.html
│   ├── mostrar_investigadores.html
│   ├── adicionar_informacoes.html
│   └── outros templates
│
└── js/
    └── arquivos JavaScript
```

---

## 🗄️ Banco de dados

O sistema utiliza **PostgreSQL** para armazenar as informações das investigações.

Entre as tabelas utilizadas estão:

- `casos`
- `suspeitos`
- `evidencias`
- `testemunhas`

A conexão com o banco é realizada através da variável de ambiente `DATABASE_URL`.

---

## 🚀 Como executar o projeto

### 1. Clone o repositório

```bash
git clone https://github.com/Kael-Beltran/investigacao-policial-vscode.git
```

### 2. Entre na pasta

```bash
cd investigacao-policial-vscode
```

### 3. Crie um ambiente virtual

```bash
python -m venv venv
```

### 4. Ative o ambiente virtual

No Windows:

```bash
venv\Scripts\activate
```

### 5. Instale as dependências

```bash
pip install -r requirements.txt
```

### 6. Configure as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DATABASE_URL=sua_string_de_conexao
SECRET_KEY=sua_chave_secreta
```

### 7. Execute o projeto

```bash
python app.py
```

O sistema estará disponível em:

```text
http://127.0.0.1:5000
```

---

## ☁️ Deploy

O projeto pode ser publicado utilizando o **Vercel**, com o banco de dados hospedado no **Neon PostgreSQL**.

---

## 👨‍💻 Desenvolvimento

Projeto desenvolvido como parte de um projeto de investigação e desenvolvimento de um sistema web para gerenciamento de informações policiais.

---

## 📄 Licença

Este projeto foi desenvolvido para fins educacionais.
