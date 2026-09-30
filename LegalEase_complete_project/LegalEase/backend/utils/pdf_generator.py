from io import BytesIO
from fpdf import FPDF

from backend.utils.text_utils import sanitize_text


class LegalEasePDF(FPDF):
    def __init__(self, doc_type: str):
        super().__init__()
        self.doc_type = doc_type

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 9, "LEGALEASE", align="C")
        self.ln(7)
        self.set_font("Helvetica", "B", 12)
        self.multi_cell(0, 7, self.doc_type.upper(), align="C")
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "", 8)
        self.cell(
            0,
            10,
            f"LegalEase | AI-generated draft | Page {self.page_no()}",
            align="C",
        )


def format_pdf(text: str, doc_type: str) -> bytes:
    pdf = LegalEasePDF(doc_type)
    pdf.set_auto_page_break(auto=True, margin=18)
    pdf.set_margins(18, 18, 18)
    pdf.add_page()

    pdf.set_font("Helvetica", "", 11)

    for raw in sanitize_text(text).splitlines():
        line = raw.strip()

        if not line:
            pdf.ln(3)
            continue

        if line.isupper() and len(line) < 120:
            pdf.set_font("Helvetica", "B", 12)
            pdf.multi_cell(0, 7, line)
            pdf.ln(1)
            pdf.set_font("Helvetica", "", 11)
        elif line.startswith(("- ", "* ")):
            pdf.multi_cell(0, 6, "  - " + line[2:].strip())
        else:
            pdf.multi_cell(0, 6, line)

    return bytes(pdf.output(dest="S"))
