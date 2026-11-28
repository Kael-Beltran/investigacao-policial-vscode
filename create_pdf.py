from fpdf import FPDF
from io import BytesIO


def criar_pdf(nomes):
    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(
        w=0,
        h=15,
        text="Relatorio de Nomes",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.ln(5)

    pdf.set_font("Helvetica", size=12)
    pdf.cell(
        w=0,
        h=10,
        text=f"Quantidade de registros: {len(nomes)}",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.set_fill_color(220, 230, 241)

    pdf.cell(w=20, h=10, text="ID", border=1, align="C", fill=True)
    pdf.cell(
        w=0,
        h=10,
        text="Nome",
        border=1,
        align="C",
        fill=True,
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.set_font("Helvetica", size=11)

    for indice, nome in enumerate(nomes, start=1):
        pdf.cell(w=20, h=9, text=str(indice), border=1, align="C")
        pdf.cell(
            w=0,
            h=9,
            text=nome,
            border=1,
            new_x="LMARGIN",
            new_y="NEXT",
        )

    return BytesIO(pdf.output())


def criar_pdf_caso(caso, suspeitos, evidencias, testemunhas, equipe=None):
    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(
        w=0,
        h=12,
        text=f"Caso #{caso['id']}",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(
        w=0,
        h=12,
        text=caso["titulo"] or "Sem titulo",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(
        w=0,
        h=8,
        text="Tipo de crime:",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(
        w=0,
        h=8,
        text=caso["tipo_crime"] or "Nao informado",
    )

    pdf.set_font("Helvetica", "B", 11)
    pdf.cell(
        w=0,
        h=8,
        text="Descricao:",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(
        w=0,
        h=8,
        text=caso["descricao"] or "Nao informado",
    )

    pdf.ln(8)

    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(
        w=0,
        h=10,
        text="00. Equipe do caso",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.set_font("Helvetica", size=11)

    def texto_seguro(valor):

        return str(valor).encode("latin-1", "replace").decode("latin-1")

    if equipe:
        for investigador in equipe:
            linha = investigador["nome"] or "Nao informado"
            if investigador.get("cargo"):
                linha += f" - {investigador['cargo']}"
            pdf.multi_cell(
                w=0,
                h=8,
                text=texto_seguro(linha),
                border=1,
                new_x="LMARGIN",
                new_y="NEXT",
            )
    else:
        pdf.cell(
            w=0,
            h=8,
            text="Nenhum investigador vinculado.",
            border=1,
            new_x="LMARGIN",
            new_y="NEXT",
        )

    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(
        w=0,
        h=10,
        text="01. Suspeitos",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.set_font("Helvetica", size=11)

    if suspeitos:
        for suspeito in suspeitos:
            pdf.multi_cell(
                w=0,
                h=8,
                text=suspeito["nome"] or "Nao informado",
                border=1,
            )
    else:
        pdf.cell(
            w=0,
            h=8,
            text="Nenhum suspeito registrado.",
            border=1,
            new_x="LMARGIN",
            new_y="NEXT",
        )

    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(
        w=0,
        h=10,
        text="02. Evidencias",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.set_font("Helvetica", size=11)

    if evidencias:
        for evidencia in evidencias:
            pdf.multi_cell(
                w=0,
                h=8,
                text=evidencia["descricao"] or "Nao informado",
                border=1,
            )
    else:
        pdf.cell(
            w=0,
            h=8,
            text="Nenhuma evidencia registrada.",
            border=1,
            new_x="LMARGIN",
            new_y="NEXT",
        )

    pdf.ln(6)

    pdf.set_font("Helvetica", "B", 15)
    pdf.cell(
        w=0,
        h=10,
        text="03. Testemunhas",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.set_font("Helvetica", size=11)

    if testemunhas:
        for testemunha in testemunhas:
            pdf.multi_cell(
                w=0,
                h=8,
                text=testemunha["nome"] or "Nao informado",
                border=1,
            )
    else:
        pdf.cell(
            w=0,
            h=8,
            text="Nenhuma testemunha registrada.",
            border=1,
            new_x="LMARGIN",
            new_y="NEXT",
        )

    return BytesIO(pdf.output())


def criar_pdf_investigador(investigador, casos):
    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4",
    )
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 18)
    pdf.cell(
        w=0,
        h=12,
        text="Relatorio do Investigador",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.ln(5)
    pdf.set_font("Helvetica", "B", 12)
    pdf.multi_cell(
        w=0,
        h=8,
        text=investigador["nome"] or "Sem nome",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.set_font("Helvetica", size=11)
    pdf.multi_cell(
        w=0,
        h=7,
        text=f"Matricula: {investigador.get('matricula') or 'Nao informada'}",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.multi_cell(
        w=0,
        h=7,
        text=f"Cargo: {investigador.get('cargo') or 'Nao informado'}",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.multi_cell(
        w=0,
        h=7,
        text=f"Telefone: {investigador.get('telefone') or 'Nao informado'}",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.multi_cell(
        w=0,
        h=7,
        text=f"Email: {investigador.get('email') or 'Nao informado'}",
        new_x="LMARGIN",
        new_y="NEXT",
    )
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 14)
    pdf.cell(
        w=0,
        h=10,
        text=f"Casos trabalhados: {len(casos)}",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    if casos:
        for caso in casos:
            pdf.set_font("Helvetica", "B", 11)
            pdf.multi_cell(
                w=0,
                h=8,
                text=f"Caso #{caso['id']} - {caso['titulo'] or 'Sem titulo'}",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            pdf.set_font("Helvetica", size=10)
            pdf.multi_cell(
                w=0,
                h=7,
                text=f"Tipo de crime: {caso['tipo_crime'] or 'Nao informado'}",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            pdf.multi_cell(
                w=0,
                h=7,
                text=f"Descricao: {caso['descricao'] or 'Nao informada'}",
                new_x="LMARGIN",
                new_y="NEXT",
            )
            pdf.ln(3)
    else:
        pdf.set_font("Helvetica", size=11)
        pdf.multi_cell(
            w=0,
            h=8,
            text="Nenhum caso vinculado a este investigador.",
            new_x="LMARGIN",
            new_y="NEXT",
        )

    return BytesIO(pdf.output())

def criar_pdf_registro(titulo, registros, campos):
    """Gera um PDF simples com os campos informados de um ou mais registros."""
    pdf = FPDF(orientation="P", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    def texto_seguro(valor):
        texto = "Não informado" if valor is None or valor == "" else str(valor)
        return texto.encode("latin-1", "replace").decode("latin-1")

    pdf.set_font("Helvetica", "B", 18)
    pdf.multi_cell(0, 11, texto_seguro(titulo), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_font("Helvetica", size=11)
    pdf.cell(0, 8, f"Quantidade de registros: {len(registros)}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    if not registros:
        pdf.multi_cell(0, 8, "Nenhum registro encontrado.", new_x="LMARGIN", new_y="NEXT")
    else:
        for indice, registro in enumerate(registros, start=1):
            if pdf.get_y() > 255:
                pdf.add_page()
            pdf.set_font("Helvetica", "B", 13)
            pdf.multi_cell(0, 9, f"Registro {indice}", border=1, new_x="LMARGIN", new_y="NEXT")
            pdf.set_font("Helvetica", size=10)
            for rotulo, chave in campos:
                valor = texto_seguro(registro.get(chave))
                pdf.multi_cell(0, 7, f"{rotulo}: {valor}", border="LR", new_x="LMARGIN", new_y="NEXT")
            pdf.cell(0, 2, "", border="B", new_x="LMARGIN", new_y="NEXT")
            pdf.ln(4)

    return BytesIO(pdf.output())
