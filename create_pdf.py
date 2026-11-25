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


def criar_pdf_caso(caso, suspeitos, evidencias, testemunhas):
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