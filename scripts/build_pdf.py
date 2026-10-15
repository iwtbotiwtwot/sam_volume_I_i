#!/usr/bin/env python3
"""Build the seven-page Chapter I reader draft.

ReportLab text/tables and vector MathText equations. Sources remain editable.
Optional isolated dependencies: matplotlib, svglib. See ../README.md.
"""
from pathlib import Path
import argparse
import hashlib
import html
import io
import json
import re
import sys

import matplotlib
matplotlib.use('Agg')
matplotlib.rcParams['mathtext.fontset'] = 'stix'
from matplotlib import mathtext
from matplotlib.font_manager import FontProperties
from fontTools.ttLib import TTFont as InspectFont
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    Flowable, Paragraph, Spacer, Table, TableStyle, SimpleDocTemplate,
    KeepTogether, PageBreak,
)
from reportlab.graphics import renderPDF
from svglib.svglib import svg2rlg

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'build'
TMP = ROOT / 'build' / 'equation_cache'
OUT.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)
FONTS = ROOT / 'assets' / 'fonts'
for name, fn in [
    ('Body', 'NotoSerif-Regular.ttf'), ('BodyBold', 'NotoSerif-Bold.ttf'),
    ('BodyItalic', 'NotoSerif-Italic.ttf'), ('Sans', 'NotoSans-Regular.ttf'),
    ('SansBold', 'NotoSans-Bold.ttf'), ('Math', 'NotoSansMath-Regular.ttf'),
]:
    pdfmetrics.registerFont(TTFont(name, str(FONTS / fn)))
pdfmetrics.registerFontFamily('Body', normal='Body', bold='BodyBold', italic='BodyItalic', boldItalic='BodyBold')
pdfmetrics.registerFontFamily('Sans', normal='Sans', bold='SansBold', italic='Sans', boldItalic='SansBold')
CMAP = set(InspectFont(FONTS / 'NotoSerif-Regular.ttf').getBestCmap())
MATHCMAP = set(InspectFont(FONTS / 'NotoSansMath-Regular.ttf').getBestCmap())
INK = colors.HexColor('#17212B')
BLUE = colors.HexColor('#264E64')
MUTED = colors.HexColor('#586772')
RULE = colors.HexColor('#B4C2CB')
PAPER = (612, 792)
MARGIN = 41
GAP = 21
CW = (PAPER[0] - 2*MARGIN - GAP)/2

STYLES = {
    'body': ParagraphStyle('body', fontName='Body', fontSize=10, leading=13.5,
                           textColor=INK, spaceAfter=6.1, splitLongWords=False),
    'h2': ParagraphStyle('h2', fontName='BodyBold', fontSize=11.15, leading=14.1,
                         textColor=BLUE, spaceBefore=2, spaceAfter=7.5),
    'h3': ParagraphStyle('h3', fontName='BodyBold', fontSize=10.2, leading=13.3,
                         textColor=BLUE, spaceBefore=6, spaceAfter=5),
    'table': ParagraphStyle('table', fontName='Sans', fontSize=7.65, leading=10.6, textColor=INK),
    'tablehead': ParagraphStyle('tablehead', fontName='SansBold', fontSize=7.65, leading=10.6, textColor=INK),
    'abstract': ParagraphStyle('abstract', fontName='Body', fontSize=9.2, leading=12.7, textColor=INK),
    'title': ParagraphStyle('title', fontName='BodyBold', fontSize=20, leading=24, textColor=BLUE),
    'sub': ParagraphStyle('sub', fontName='Sans', fontSize=8.7, leading=12, textColor=MUTED),
}
LAYOUT = []

def cleanup(s):
    return s.replace('\u2011','-').replace('\u2013','-').replace('\u2014','-')

def markup(s):
    s = cleanup(s)
    # Retain the small supported HTML vocabulary used in editable manuscript.
    s = html.escape(s)
    s = re.sub(r'&lt;(/?(?:sub|sup|i|b))&gt;', r'<\1>', s)
    s = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', s)
    s = re.sub(r'(?<!\*)\*([^*]+)\*(?!\*)', r'<i>\1</i>', s)
    s = re.sub(r'`([^`]+)`', r'<font name="Sans">\1</font>', s)
    # Keep citations together and attached to the preceding word.
    s = re.sub(r'\[[1-9][0-9,;§ -]*\]', lambda m: m.group(0).replace(' ', '&#160;'), s)
    s = re.sub(r' (?=\[[1-9])', '&#160;', s)
    # Math symbols outside the text font receive an embedded math font.
    s = ''.join((f'<font name="Math">{ch}</font>' if ord(ch) not in CMAP and ord(ch) in MATHCMAP else ch) for ch in s)
    return s

class Equation(Flowable):
    def __init__(self, tex, size=10.7):
        super().__init__()
        tex = re.sub(r'\\le(?![A-Za-z])', r'\\leq', tex)
        tex = re.sub(r'\\ge(?![A-Za-z])', r'\\geq', tex)
        tex = tex.replace(r'\frac{', r'\dfrac{')
        self.tex = tex
        self.size = size
        self.spaceBefore = 1.5
        self.spaceAfter = 4.5
        h = hashlib.sha256(('stix-v1|'+str(size)+tex).encode()).hexdigest()[:20]
        f = TMP / f'eq-{h}.svg'
        if not f.exists():
            mathtext.math_to_image('$'+tex+'$', str(f), prop=FontProperties(size=size), format='svg', color='#17212b')
        self.drawing = svg2rlg(str(f))
        self.natural = (self.drawing.width, self.drawing.height)
    def wrap(self, aw, ah):
        self.factor = min(1, aw/self.natural[0])
        self.width = min(aw, self.natural[0])
        self.height = self.natural[1]*self.factor + 3
        if self.size*self.factor < 8.1:
            raise ValueError(f'Equation too wide ({self.size*self.factor:.1f} pt): {self.tex}')
        return aw, self.height
    def draw(self):
        c = self.canv
        c.saveState()
        c.translate((CW-self.width)/2 if getattr(self, 'core', False) else 0, 1)
        c.scale(self.factor, self.factor)
        renderPDF.draw(self.drawing, c, 0, 0)
        c.restoreState()

def parse(text, companion=False):
    lines = text.strip().splitlines()
    out=[]
    i=0
    while i<len(lines):
        l=lines[i].strip()
        if not l or l.startswith('<!--'):
            i+=1; continue
        if l.startswith('$$'):
            equation=l[2:]
            while not equation.endswith('$$'):
                i+=1
                if i>=len(lines): raise ValueError('Unclosed equation')
                equation+=' '+lines[i].strip()
            tex=equation[:-2].strip()
            eq=Equation(tex, size=11.1 if companion else 10.6)
            eq.core=not companion
            out.append(eq); i+=1; continue
        if l.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].strip().startswith('|'):
                cells=[x.strip() for x in lines[i].strip().strip('|').split('|')]
                if not all(re.match(r'^:?-+:?$',x) for x in cells): rows.append(cells)
                i+=1
            n=len(rows[0])
            avail=PAPER[0]-2*MARGIN if companion else CW
            if n==2: widths=[avail*.45, avail*.55]
            elif n==3: widths=[avail*.16, avail*.42, avail*.42]
            else: widths=[avail/n]*n
            data=[[Paragraph(markup(c), STYLES['tablehead' if ri==0 else 'table']) for c in row] for ri,row in enumerate(rows)]
            t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
            t.setStyle(TableStyle([
                ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#EDF2F5')),
                ('LINEBELOW',(0,0),(-1,0),.5,RULE),
                ('LINEBELOW',(0,-1),(-1,-1),.5,RULE),
                ('VALIGN',(0,0),(-1,-1),'TOP'),
                ('LEFTPADDING',(0,0),(-1,-1),5),('RIGHTPADDING',(0,0),(-1,-1),5),
                ('TOPPADDING',(0,0),(-1,-1),4),('BOTTOMPADDING',(0,0),(-1,-1),4),
            ]))
            out.extend([t,Spacer(1,7)]); continue
        if l.startswith('#'):
            level=len(l)-len(l.lstrip('#'))
            key='title' if level==1 else ('h2' if level==2 else 'h3')
            out.append(Paragraph(markup(l[level:].strip()),STYLES[key])); i+=1;continue
        if l=='::: page':
            out.append(PageBreak()); i+=1;continue
        para=l
        while i+1<len(lines) and lines[i+1].strip() and not lines[i+1].strip().startswith(('#','$$','|','<!--',':::')):
            i+=1;para+=' '+lines[i].strip()
        if re.match(r'^[-*] ',para): para='• '+para[2:]
        style=STYLES['body']
        out.append(Paragraph(markup(para),style));i+=1
    return out

def frame(c, flow, x, top, width, bottom, label):
    y=top
    for f in flow:
        before=f.getSpaceBefore()
        after=f.getSpaceAfter()
        w,h=f.wrap(width,y-bottom)
        y-=before
        if y-h<bottom-0.1:
            raise ValueError(f'Overflow {label}: {y-h:.1f} < {bottom}; item {str(getattr(f,"text",getattr(f,"tex",f)))[:100]}')
        f.drawOn(c,x,y-h)
        y-=h+after
    LAYOUT.append({'frame':label,'bottom_y':round(y,2),'unused_height':round(y-bottom,2)})

def chrome(c, doc=None, kind='CHAPTER I', page=None):
    p=page or doc.page
    c.setStrokeColor(RULE);c.setLineWidth(.5)
    c.line(MARGIN,754,612-MARGIN,754)
    c.setFont('SansBold',7.5);c.setFillColor(BLUE)
    c.drawString(MARGIN,765,'SAM  /  VOLUME I')
    c.setFont('Sans',7.5);c.setFillColor(MUTED)
    c.drawRightString(612-MARGIN,765,kind+'  ·  FINAL DRAFT')
    c.line(MARGIN,37,612-MARGIN,37)
    c.setFont('Sans',7.2)
    c.drawString(MARGIN,24,'Brady · ChatGPT · Codex  |  15 October 2026')
    c.drawRightString(612-MARGIN,24,str(p))

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=ROOT/'build/Chapter_I.pdf')
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    core=(ROOT/'manuscript/chapter_I.md').read_text(encoding='utf-8')
    pieces=re.split(r'<!-- PAGE (\d+) (LEFT|RIGHT) -->',core)
    c=canvas.Canvas(str(args.output),pagesize=PAPER,pageCompression=1,invariant=1)
    c.setTitle('SAM Volume I Chapter I: Original Write histories and an interacting source-field action')
    c.setAuthor('Sean Brady; OpenAI ChatGPT and Codex')
    c.setSubject('Final draft, 15 October 2026; source-bound interacting clock and action')
    for j in range(1,len(pieces),3):
        page,side,body=int(pieces[j]),pieces[j+1],pieces[j+2]
        STYLES['body'].fontSize = 9.7 if page==1 else 10
        STYLES['body'].leading = 13.1 if page==1 else 13.5
        STYLES['body'].spaceAfter = 5.5 if page==1 else 6.1
        if side=='LEFT':
            chrome(c,kind='CHAPTER I',page=page)
            if page==1:
                title=Paragraph('Original Write histories and an<br/>interacting source-field action',STYLES['title'])
                title.wrap(530,100);title.drawOn(c,MARGIN,691)
                subtitle=Paragraph('Volume I, Chapter I · 15 October 2026<br/>Sean Brady · Originator and conceptual director<br/>OpenAI ChatGPT and Codex · AI research collaborators and co-authors',STYLES['sub'])
                subtitle.wrap(530,60);subtitle.drawOn(c,MARGIN,645)
                abstract=re.search(r'## Abstract\s+(.*?)\s*<!--',core,re.S).group(1)
                para=Paragraph('<b>Abstract.</b> '+markup(abstract),STYLES['abstract'])
                _,h=para.wrap(530,140);para.drawOn(c,MARGIN,633-h)
                c.setStrokeColor(RULE);c.line(MARGIN,621-h,571,621-h)
                top=608-h
            else: top=737
        x=MARGIN if side=='LEFT' else MARGIN+CW+GAP
        frame(c,parse(body),x,top,CW,51,f'core {page} {side}')
        if side=='RIGHT': c.showPage()
    c.save()
    (ROOT/'build/layout_metrics.json').write_text(json.dumps(LAYOUT,indent=2)+'\n')
    print(json.dumps(LAYOUT,indent=2))

if __name__=='__main__':main()
