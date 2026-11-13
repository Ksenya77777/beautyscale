import re,sys,html
src,dst=sys.argv[1],sys.argv[2]
def inline(t):
    t=html.escape(t,quote=False)
    t=re.sub(r'`([^`]+)`',r'<code>\1</code>',t)
    t=re.sub(r'\*\*([^*]+)\*\*',r'<b>\1</b>',t)
    t=re.sub(r'(https?://[^\s<)]+[^\s<).,])',r'<a href="\1">\1</a>',t)
    return t
out=[];lines=open(src,encoding='utf-8').read().split('\n');i=0;lst=None
def close():
    global lst
    if lst: out.append('</%s>'%lst);lst=None
while i<len(lines):
    l=lines[i]
    if l.startswith('|'):
        close();rows=[]
        while i<len(lines) and lines[i].startswith('|'):
            rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')]);i+=1
        out.append('<table><thead><tr>'+''.join('<th>%s</th>'%inline(c) for c in rows[0])+'</tr></thead><tbody>')
        for r in rows[2:]: out.append('<tr>'+''.join('<td>%s</td>'%inline(c) for c in r)+'</tr>')
        out.append('</tbody></table>');continue
    m=re.match(r'(#+) (.*)',l)
    if m: close();n=len(m.group(1));out.append('<h%d>%s</h%d>'%(n,inline(m.group(2)),n))
    elif re.match(r'- \[ \] ',l): 
        if lst!='ul': close();out.append('<ul class="chk">');lst='ul'
        out.append('<li>☐ '+inline(l[6:])+'</li>')
    elif l.startswith('- '):
        if lst!='ul': close();out.append('<ul>');lst='ul'
        out.append('<li>'+inline(l[2:])+'</li>')
    elif re.match(r'\d+\. ',l):
        if lst!='ol': close();out.append('<ol>');lst='ol'
        out.append('<li>'+inline(re.sub(r'^\d+\. ','',l))+'</li>')
    elif l.strip()=='': close()
    else: close();out.append('<p>'+inline(l)+'</p>')
    i+=1
close()
css='''@page{size:A4;margin:14mm}body{font-family:-apple-system,Helvetica,Arial,sans-serif;font-size:15px;line-height:1.5;color:#1f1a1d;max-width:800px;margin:0 auto;padding:12px}
h1{font-size:24px}h2{font-size:19px;margin-top:26px;border-bottom:1px solid #ddd;padding-bottom:4px}p,li{margin:6px 0}ul.chk{list-style:none;padding-left:4px}
table{border-collapse:collapse;width:100%;margin:10px 0;font-size:14px}th,td{border:1px solid #ccc;padding:6px 8px;text-align:left;vertical-align:top}th{background:#f4eae7}
code{background:#f3f0f0;padding:1px 4px;border-radius:3px;word-break:break-all}a{color:#54263A;word-break:break-all}tr,li{break-inside:avoid}'''
open(dst,'w',encoding='utf-8').write('<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Запуск рекламы beautyscale.by</title><style>%s</style></head><body>%s</body></html>'%(css,'\n'.join(out)))
