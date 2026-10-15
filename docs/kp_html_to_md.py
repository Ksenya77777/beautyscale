"""Собирает docs/KP_beautyscale.md из docs/KP_beautyscale.html (markdown-копия для чтения вместо PDF)."""
import re, sys, os
D=os.path.dirname(os.path.abspath(__file__))+'/'
from html.parser import HTMLParser

class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.out=[]; s.row=None; s.cell=None; s.table=[]; s.in_table=False
        s.list_depth=0; s.skip=False; s.buf=[]
    def txt(s, t):
        (s.cell if s.cell is not None else s.buf).append(t)
    def flush(s):
        t=''.join(s.buf).strip()
        if t: s.out.append(t)
        s.buf=[]
    def handle_starttag(s, tag, a):
        if tag in('style','title'): s.skip=True
        if s.skip: return
        if tag in('h1','h2','h3','p','div') and s.cell is None: s.flush()
        if tag=='h1': s.txt('# ')
        if tag=='h2': s.txt('## ')
        if tag=='h3': s.txt('### ')
        if tag in('b','strong'): s.txt('**')
        if tag=='li':
            if s.cell is not None: s.txt('<br>- ')
            else: s.flush(); s.txt('- ')
        if tag=='table': s.flush(); s.table=[]
        if tag=='tr': s.row=[]
        if tag in('td','th'): s.cell=[]; s.span=int(dict(a).get('colspan',1))
        if tag=='br': s.txt(' ')
    def handle_endtag(s, tag):
        if tag in('style','title'): s.skip=False; return
        if s.skip: return
        if tag in('b','strong'): s.txt('**')
        if tag in('td','th'):
            c=' '.join(''.join(s.cell).split()).replace('|','/')
            s.row.append(c)
            for _ in range(s.span-1): s.row.append('(то же)')
            s.cell=None
        if tag=='tr': s.table.append(s.row)
        if tag=='table':
            t=s.table; n=max(len(r) for r in t)
            lines=['| '+' | '.join(r+['']*(n-len(r)))+' |' for r in t]
            lines.insert(1,'|'+'---|'*n)
            s.out.append('\n'.join(lines))
        if tag in('h1','h2','h3','p','div','li') and s.cell is None: s.flush()
    def handle_data(s, d):
        if s.skip: return
        s.txt(re.sub(r'\s+',' ',d))

p=P(); p.feed(open(D+'KP_beautyscale.html',encoding='utf-8').read()); p.flush()
md='\n\n'.join(x for x in p.out)
md=re.sub(r'\n\n(- )',r'\n\1',md)
md=md.replace('\n\n\n','\n\n')
head='<!-- Читаемая копия КП. Генерируется из KP_beautyscale.html командой: python3 docs/kp_html_to_md.py. Не править руками. -->\n\n'
open(D+'KP_beautyscale.md','w',encoding='utf-8').write(head+md+'\n')
