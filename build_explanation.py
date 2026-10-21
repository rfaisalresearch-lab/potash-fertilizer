"""Typeset the explanation using the same PDF tools as the CPRIL report."""
from pathlib import Path
from xml.sax.saxutils import escape
import csv,re
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER,TA_JUSTIFY,TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,PageBreak,Image,Table,TableStyle

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'Potash_Explanation.pdf'
W,H=595.276,790.866
M=20*mm
CW=W-2*M
INK=colors.black
ORCID='https://orcid.org/0009-0005-1111-1501'

styles={
 'title':ParagraphStyle('title',fontName='Times-Bold',fontSize=15.5,leading=18.5,alignment=TA_CENTER,textColor=INK,spaceAfter=10),
 'author':ParagraphStyle('author',fontName='Times-Italic',fontSize=12,leading=15,alignment=TA_CENTER,textColor=INK,spaceAfter=5),
 'affiliation':ParagraphStyle('affiliation',fontName='Times-Italic',fontSize=10.5,leading=12.5,alignment=TA_CENTER,textColor=INK,spaceAfter=0),
 'orcid':ParagraphStyle('orcid',fontName='Times-Roman',fontSize=10,leading=12,textColor=INK),
 'heading':ParagraphStyle('heading',fontName='Times-Bold',fontSize=11.4,leading=14,spaceAfter=8),
 'body':ParagraphStyle('body',fontName='Times-Roman',fontSize=11,leading=13.6,alignment=TA_JUSTIFY,textColor=INK,firstLineIndent=12,spaceAfter=7),
 'credit':ParagraphStyle('credit',fontName='Times-Roman',fontSize=10.6,leading=13.2,alignment=TA_LEFT,textColor=INK,spaceAfter=10),
 'ref':ParagraphStyle('ref',fontName='Times-Roman',fontSize=10.6,leading=13.1,alignment=TA_LEFT,leftIndent=15,firstLineIndent=-15,spaceAfter=12,splitLongWords=True),
}

def page(canvas,doc):
 canvas.saveState()
 canvas.setFillColor(INK)
 canvas.setFont('Times-Italic',9)
 canvas.drawRightString(W-M,H-29*mm,'SCH3U')
 canvas.drawRightString(W-M,H-34*mm,'18 October 2026' if doc.page==1 else '19 October 2026')
 # ORCID belongs in the upper-left header, above the horizontal rule.
 orcid_y=H-34*mm
 canvas.drawImage(str(ROOT/'orcid.png'),M,orcid_y-2,width=12,height=12,mask='auto')
 canvas.setFont('Times-Roman',9)
 canvas.drawString(M+16,orcid_y,'0009-0005-1111-1501')
 canvas.linkURL(ORCID,(M,orcid_y-3,M+125,orcid_y+11),relative=0,thickness=0)
 canvas.setStrokeColor(colors.HexColor('#777777'))
 canvas.setLineWidth(.45)
 canvas.line(M,H-36*mm,W-M,H-36*mm)
 canvas.setFont('Times-Roman',9)
 canvas.drawRightString(W-M,13*mm,str(doc.page))
 canvas.restoreState()

content=(ROOT/'explanation.txt').read_text().strip()
words=len(content.split())
assert 300<=words<=500
pars=content.split('\n\n')
# Keep ion charges and the arrow readable in the PDF.
def body_markup(text):
 text=escape(text)
 text=text.replace('→','<font name="Symbol">&#8594;</font>').replace('K+(aq)','K<super>+</super>(aq)').replace('Cl−(aq)','Cl<super>-</super>(aq)')

 return text

story=[Spacer(1,25),Paragraph('Potash Fertilizer<br/>From Underground Salts to Crop Nutrients',styles['title']),Paragraph('Rayan Faisal',styles['author'])]
story.append(Spacer(1,9))
story.append(Paragraph('Northern Collegiate Institute &amp; Vocational School<br/>940 Michigan Avenue, Sarnia, ON N7S 2B1<br/>e-mail: <link href="mailto:RFaisalresearch@gmail.com" color="#000000"><u>RFaisalresearch@gmail.com</u></link>',styles['affiliation']))
story.extend([Spacer(1,21),Paragraph('Explanation',styles['heading'])])
for paragraph in pars:story.append(Paragraph(body_markup(paragraph),styles['body']))
story.extend([PageBreak(),Spacer(1,15),Paragraph('Acknowledgements',styles['title']),Spacer(1,13)])
credits=(ROOT/'Acknowledgements.html').read_text().strip().split('\n\n')
for paragraph in credits:story.append(Paragraph(paragraph,styles['credit']))
story.extend([PageBreak(),Spacer(1,15),Paragraph('References',styles['title']),Spacer(1,13)])
refs=list(csv.DictReader((ROOT/'references.tsv').open(),delimiter='\t'))
for ref in refs:
 italic=ref['italic_title']
 entry=escape(ref['author_date']+' '+ref['title'])
 entry=entry.replace(escape(italic),'<i>'+escape(italic)+'</i>')
 url=escape(ref['url'])
 story.append(Paragraph(entry+f'<br/><link href="{url}" color="#000000">{url}</link>',styles['ref']))

doc=SimpleDocTemplate(str(OUT),pagesize=(W,H),leftMargin=M,rightMargin=M,topMargin=38*mm,bottomMargin=19*mm,title='Potash Fertilizer',author='Rayan Faisal',subject='SCH3U explanation and APA 7 references')
doc.build(story,onFirstPage=page,onLaterPages=page)
print(f'Built explanation with {words} words and {len(refs)} sources')
