from io import BytesIO
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_SECTION
from docx.shared import Inches, Pt
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from backend.utils.text_utils import sanitize_text


def _set_cell_shading(cell, fill="EAEAEA"):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), fill)
    tc_pr.append(shd)


def format_docx(text: str, doc_type: str, terms: str = "") -> bytes:
    doc = Document()

    section = doc.sections[0]
    section.top_margin = Inches(0.75)
    section.bottom_margin = Inches(0.75)
    section.left_margin = Inches(0.85)
    section.right_margin = Inches(0.85)

    styles = doc.styles
    normal = styles["Normal"]
    normal.font.name = "Times New Roman"
    normal.font.size = Pt(11)

    title = doc.add_paragraph()
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = title.add_run(doc_type.upper())
    run.bold = True
    run.font.name = "Times New Roman"
    run.font.size = Pt(16)

    subtitle = doc.add_paragraph()
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sr = subtitle.add_run("LegalEase - AI-Assisted Legal Document Draft")
    sr.italic = True
    sr.font.size = Pt(9)

    for raw in sanitize_text(text).splitlines():
        line = raw.strip()
        if not line:
            doc.add_paragraph()
            continue

        if line.isupper() and len(line) < 120:
            p = doc.add_paragraph()
            r = p.add_run(line)
            r.bold = True
            r.font.name = "Times New Roman"
            r.font.size = Pt(12)
        elif line[:2].isdigit() and "." in line[:5]:
            p = doc.add_paragraph()
            r = p.add_run(line)
            r.bold = True
        elif line.startswith(("- ", "* ")):
            doc.add_paragraph(line[2:].strip(), style="List Bullet")
        else:
            doc.add_paragraph(line)

    clean_terms = [t.strip() for t in terms.split(";") if t.strip()]
    if clean_terms:
        doc.add_page_break()
        h = doc.add_paragraph()
        rr = h.add_run("TERMS SUMMARY")
        rr.bold = True
        rr.font.size = Pt(12)

        table = doc.add_table(rows=1, cols=2)
        table.style = "Table Grid"
        hdr = table.rows[0].cells
        hdr[0].text = "No."
        hdr[1].text = "Term / Condition"
        _set_cell_shading(hdr[0])
        _set_cell_shading(hdr[1])

        for i, term in enumerate(clean_terms, 1):
            cells = table.add_row().cells
            cells[0].text = str(i)
            cells[1].text = term

    footer = section.footer.paragraphs[0]
    footer.alignment = WD_ALIGN_PARAGRAPH.CENTER
    fr = footer.add_run("LegalEase | AI-generated draft | Review before signing")
    fr.font.size = Pt(8)

    output = BytesIO()
    doc.save(output)
    return output.getvalue()


def format_txt(text: str) -> bytes:
    return sanitize_text(text).encode("utf-8")
