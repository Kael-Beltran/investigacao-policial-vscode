from fpdf import FPDF
from io import BytesIO

def criar_pdf(nomes):
    pdf = FPDF(
        orientation='P',
        unit='mm',
        format='A4',
    )
    pdf.add_page()

    # Título do Relatório
    pdf.set_font(family="Helvetica", style="B", size=18)
    pdf.cell(
        w=0,
        h=15,
        text="Relatorio de Nomes",
        align="C",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.ln(5)

    # Quantidade de Registros
    pdf.set_font(family="Helvetica", size=12)
    pdf.cell(
        w=0,
        h=10,
        text=f"Quantidade de registros: {len(nomes)}",
        new_x="LMARGIN",
        new_y="NEXT",
    )

    pdf.ln(5)

    # Cabeçalho da Tabela
    pdf.set_font(family="Helvetica", style="B", size=12)
    pdf.set_fill_color(220, 230, 241)
    
    # Coluna ID
    pdf.cell(w=20, h=10, text="ID", border=1, align="C", fill=True)
    # Coluna Nome
    pdf.cell(w=0, h=10, text="Nome", border=1, align="C", fill=True, new_x="LMARGIN", new_y="NEXT")

    # Linhas da Tabela (Itens)
    pdf.set_font("Helvetica", size=11)
    for indice, nome in enumerate(nomes, start=1):
        pdf.cell(w=20, h=9, text=str(indice), border=1, align="C")
        pdf.cell(w=0, h=9, text=nome, border=1, new_x="LMARGIN", new_y="NEXT")

    # Gera os bytes do PDF na memória e retorna como BytesIO
    pdf_bytes = pdf.output()
    arquivo_pdf = BytesIO(pdf_bytes)

    return arquivo_pdf