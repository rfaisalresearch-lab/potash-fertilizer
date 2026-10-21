from pathlib import Path
import csv
import shutil
import subprocess
import tempfile
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parent
lines = [line for line in (ROOT / 'build.R').read_text().splitlines()
         if line.strip() and not line.lstrip().startswith('#')]
code = '\n'.join(lines) + '\n'
colours = [[(0, 0, 0)] * len(line) for line in lines]
keywords = {'FUNCTION', 'IF', 'ELSE', 'FOR', 'IN', 'WHILE', 'REPEAT',
            'NEXT', 'BREAK', 'NULL_CONST', 'LEFT_ASSIGN', 'RIGHT_ASSIGN', 'EQ_ASSIGN'}
rscript = shutil.which('Rscript') or '/usr/local/bin/Rscript'
with tempfile.TemporaryDirectory(prefix='.code-pdf-', dir=ROOT) as temp:
    source = Path(temp) / 'code.R'
    tokens_file = Path(temp) / 'tokens.csv'
    source.write_text(code)
    subprocess.run([rscript, '--vanilla', '-e',
        'a<-commandArgs(TRUE); p<-getParseData(parse(a[1],keep.source=TRUE)); '
        'p<-p[p$terminal,]; stopifnot(!any(p$token=="COMMENT")); '
        'write.csv(p,a[2],row.names=FALSE)', str(source), str(tokens_file)], check=True)
    with tokens_file.open() as stream:
        for token in csv.DictReader(stream):
            kind = token['token']
            colour = ((0, .42, 0) if kind == 'STR_CONST' else
                      (0, 0, .80) if kind == 'NUM_CONST' or kind in keywords else (0, 0, 0))
            start, end = int(token['line1']) - 1, int(token['line2']) - 1
            for row in range(start, end + 1):
                left = int(token['col1']) - 1 if row == start else 0
                right = int(token['col2']) if row == end else len(lines[row])
                colours[row][left:right] = [colour] * (right - left)

W, H = 595.276, 790.866
M = 20 * mm
top = H - 40 * mm
bottom = 14 * mm
font = 'Times-Roman'
size = min(9.2, (top - bottom) / (len(lines) * 1.05))
leading = size * 1.05
assert max(stringWidth(line, font, size) for line in lines) <= W - 2 * M
assert size >= 8
pdf = canvas.Canvas(str(ROOT / 'Potash_Infographic_R_Code.pdf'), pagesize=(W, H))
pdf.setTitle('Potash infographic R code')
pdf.setAuthor('Rayan Faisal')
pdf.setFont('Times-Italic', 9)
pdf.drawRightString(W - M, H - 29 * mm, 'SCH3U')
pdf.drawRightString(W - M, H - 34 * mm, '20 October 2026')
orcid_y = H - 34 * mm
pdf.drawImage(str(ROOT / 'orcid.png'), M, orcid_y - 2, width=12, height=12, mask='auto')
pdf.setFont(font, 9)
pdf.drawString(M + 16, orcid_y, '0009-0005-1111-1501')
pdf.linkURL('https://orcid.org/0009-0005-1111-1501',
            (M, orcid_y - 3, M + 125, orcid_y + 11), relative=0, thickness=0)
pdf.setStrokeColor(colors.HexColor('#777777'))
pdf.setLineWidth(.45)
pdf.line(M, H - 36 * mm, W - M, H - 36 * mm)
y = top
for line, row_colours in zip(lines, colours):
    text = pdf.beginText(M, y)
    text.setFont(font, size)
    start = 0
    while start < len(line):
        end = start + 1
        while end < len(line) and row_colours[end] == row_colours[start]:
            end += 1
        text.setFillColorRGB(*row_colours[start])
        text.textOut(line[start:end])
        start = end
    pdf.drawText(text)
    y -= leading
pdf.save()
print(f'Built one-page code PDF: {len(lines)} lines, Times-Roman {size:.2f} pt')
