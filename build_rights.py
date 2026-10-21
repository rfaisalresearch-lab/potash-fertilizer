from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer

ROOT = Path(__file__).resolve().parent
W, H = 595.276, 790.866
M = 20 * mm
ORCID = 'https://orcid.org/0009-0005-1111-1501'

def header(c, doc):
    c.saveState()
    c.setFillColor(colors.black)
    c.setFont('Times-Italic', 9)
    c.drawRightString(W-M, H-29*mm, 'SCH3U')
    c.drawRightString(W-M, H-34*mm, '20 October 2026')
    y = H-34*mm
    c.drawImage(str(ROOT/'orcid.png'), M, y-2, width=12, height=12, mask='auto')
    c.setFont('Times-Roman', 9)
    c.drawString(M+16, y, '0009-0005-1111-1501')
    c.linkURL(ORCID, (M, y-3, M+125, y+11), relative=0, thickness=0)
    c.setStrokeColor(colors.HexColor('#777777'))
    c.setLineWidth(.45)
    c.line(M, H-36*mm, W-M, H-36*mm)
    c.setFont('Times-Roman', 9)
    c.drawRightString(W-M, 13*mm, str(doc.page))
    c.restoreState()

body = ParagraphStyle('body', fontName='Times-Roman', fontSize=11, leading=14,
                      alignment=TA_LEFT, spaceAfter=12)
story = [Spacer(1, 25)]
for paragraph in (ROOT/'Rights_declaration.html').read_text().strip().split('\n\n'):
    story.append(Paragraph(paragraph, body))
doc = SimpleDocTemplate(str(ROOT/'Potash_Rights_and_Licensing.pdf'), pagesize=(W,H),
    leftMargin=M, rightMargin=M, topMargin=38*mm, bottomMargin=19*mm,
    title='Potash Fertilizer license notice', author='Rayan Faisal',
    subject='Potash Fertilizer original written content and infographic, CC BY 4.0')
doc.build(story, onFirstPage=header, onLaterPages=header)
print('Built rights and licensing declaration')
