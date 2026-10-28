"""Prepare the GMD JATS XML for pandoc: local figures, OASIS -> JATS tables, front matter in body, references kept."""
import re, sys, copy
from lxml import etree
src, out = sys.argv[1], sys.argv[2]
NS = {'oasis': 'http://docs.oasis-open.org/ns/oasis-exchange/table', 'xlink': 'http://www.w3.org/1999/xlink',
      'mml': 'http://www.w3.org/1998/Math/MathML'}
parser = etree.XMLParser(load_dtd=False, no_network=True, resolve_entities=False)
tree = etree.parse(src, parser)
root = tree.getroot()
X = '{http://www.w3.org/1999/xlink}href'

# figures -> local files extracted from the PDF (img-001..013 = Fig. 1..13)
for g in root.iter('graphic'):
    m = re.search(r'-f(\d\d)\.png$', g.get(X, ''))
    if m: g.set(X, f'figs/fig{int(m.group(1)):02d}.png')

def E(tag, text=None, **attrs):
    e = etree.Element(tag, **attrs)
    if text is not None: e.text = text
    return e

# a formula that is only a minus sign (table cells) becomes plain text
for f in list(root.iter('inline-formula')):
    if ''.join(f.itertext()).strip() in ('−', '-'):
        par = f.getparent(); prev = f.getprevious()
        txt = '−' + (f.tail or '')
        if prev is not None: prev.tail = (prev.tail or '') + txt
        else: par.text = (par.text or '') + txt
        par.remove(f)

# OASIS tables -> JATS tables
for ot in root.xpath('//oasis:table', namespaces=NS):
    tg = ot.find('oasis:tgroup', NS)
    cols = [c.get('colname') for c in tg.findall('oasis:colspec', NS)]
    tbl = E('table')
    for part, cell in (('thead', 'th'), ('tbody', 'td')):
        op = tg.find(f'oasis:{part}', NS)
        if op is None: continue
        jp = etree.SubElement(tbl, part)
        for row in op.findall('oasis:row', NS):
            tr = etree.SubElement(jp, 'tr')
            for ent in row.findall('oasis:entry', NS):
                c = etree.SubElement(tr, cell)
                c.text = ent.text
                for ch in ent: c.append(ch)
                ns_, ne_ = ent.get('namest'), ent.get('nameend')
                if ns_ and ne_ and ns_ in cols and ne_ in cols:
                    c.set('colspan', str(cols.index(ne_) - cols.index(ns_) + 1))
                if ent.get('morerows'):
                    c.set('rowspan', str(int(ent.get('morerows')) + 1))
    ot.getparent().replace(ot, tbl)

art = root.find('front/article-meta')
body = root.find('body')
front = E('sec', id='front-matter')
# authors with affiliation numbers
auths = []
for c in art.findall('contrib-group/contrib'):
    n = c.find('name')
    nm = f"{n.findtext('given-names')} {n.findtext('surname')}"
    affs = [r.lstrip('aff') for r in (c.get('rid') or '').split()]
    auths.append((nm, affs))
p = E('p')
for i, (nm, affs) in enumerate(auths):
    span = E('bold', nm) if False else None
    txt = nm
    if p.text is None and len(p) == 0: p.text = txt
    else: p[-1].tail = (p[-1].tail or '') + txt
    sup = E('sup', ','.join(affs)); p.append(sup)
    sup.tail = ', ' if i < len(auths) - 2 else (', and ' if i == len(auths) - 2 else '')
front.append(p)
for a in art.iter('aff'):
    front.append(E('p', f"{a.findtext('label')}{a.findtext('institution').strip()}"))
corr = art.find('author-notes/corresp')
corr_txt = ' '.join(corr.itertext()).strip() if corr is not None else 'Benjamin M. Sanderson (benjamin.sanderson@cicero.oslo.no)'
front.append(E('p', 'Correspondence: ' + re.sub(r'\s+', ' ', corr_txt)))
front.append(E('p', 'Received: 30 October 2024 – Discussion started: 15 November 2024 – Revised: 26 May 2025 – '
                    'Accepted: 3 June 2025 – Published: 5 September 2025'))
front.append(E('p', 'Geosci. Model Dev., 18, 5699–5724, 2025. https://doi.org/10.5194/gmd-18-5699-2025. '
                    '© Author(s) 2025. Distributed under the Creative Commons Attribution 4.0 License.'))
ab = art.find('abstract')
abs_sec = E('sec', id='abstract'); abs_sec.append(E('title', 'Abstract'))
for para in ab.findall('p'): abs_sec.append(copy.deepcopy(para))
body.insert(0, abs_sec); body.insert(0, front)
art.remove(ab)
for cg in art.findall('contrib-group'): art.remove(cg)

# references: keep as plain paragraphs in a References section at the end of back
back = root.find('back')
rl = back.find('ref-list')
refsec = E('sec', id='references'); refsec.append(E('title', 'References'))
for ref in rl.findall('ref'):
    mc = ref.find('mixed-citation')
    p = E('p'); p.text = mc.text
    for ch in mc:
        if ch.tag == 'ext-link':
            ch.tag = 'ext-link'  # pandoc reads ext-link as a link
        p.append(ch)
    refsec.append(p)
back.replace(rl, refsec)

# appendix -> ordinary sections at the end of the body
ag = back.find('app-group')
if ag is not None:
    for app in ag.findall('app'):
        app.tag = 'sec'
        body.append(app)
    back.remove(ag)

# carry section, figure and table numbers into the visible text
for sec in root.iter('sec'):
    lab, tit = sec.find('label'), sec.find('title')
    if lab is not None and tit is not None:
        sep = ': ' if lab.text.startswith('Appendix') else ' '
        tit.text = lab.text + sep + (tit.text or '')
        sec.remove(lab)
for el in list(root.iter('fig')) + list(root.iter('table-wrap')):
    lab = el.find('label'); cap = el.find('caption')
    if lab is not None and cap is not None and len(cap):
        first = cap[0]
        b = E('bold', lab.text + '. '); b.tail = first.text; first.text = None; first.insert(0, b)
        el.remove(lab)
for df in root.iter('disp-formula'):
    lab = df.find('label')
    if lab is not None:
        lab.getparent().remove(lab)

tree.write(out, encoding='UTF-8', xml_declaration=True)
