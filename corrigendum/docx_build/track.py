"""Tracked-change helpers for python-docx documents: word-level diffs wrapped in w:ins / w:del."""
import copy, difflib, re, itertools
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

AUTHOR = 'flat10MIP corrigendum'
DATE = '2026-10-15T00:00:00Z'
MATH = '□'
_ids = itertools.count(9000)

def _mark(tag):
    e = OxmlElement(tag)
    e.set(qn('w:id'), str(next(_ids))); e.set(qn('w:author'), AUTHOR); e.set(qn('w:date'), DATE)
    return e

def atoms(p):
    """Ordered (element, text) atoms of a paragraph: runs with text, and equations (one placeholder char)."""
    out = []
    for el in p.iter():
        if el.tag == qn('m:oMath') and el.getparent().tag != qn('m:oMathPara'):
            out.append((el, MATH))
        elif el.tag == qn('w:r') and not any(a.tag in (qn('m:oMath'), qn('w:del')) for a in el.iterancestors()):
            t = ''.join((x.text or '') if x.tag == qn('w:t') else '\t' for x in el if x.tag in (qn('w:t'), qn('w:tab')))
            if t: out.append((el, t))
    return out

def ptext(p):
    return ''.join(t for _, t in atoms(p))

def _split(run, k):
    """Split a text run at character k; returns (left, right) runs."""
    ts = run.findall(qn('w:t'))
    assert len(ts) == 1 and len([x for x in run if x.tag == qn('w:tab')]) == 0, 'complex run'
    txt = ts[0].text
    right = copy.deepcopy(run)
    ts[0].text = txt[:k]; ts[0].set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    rt = right.find(qn('w:t')); rt.text = txt[k:]; rt.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    run.addnext(right)
    return run, right

def _isolate(p, a, b):
    """Make chars [a, b) of the paragraph text consist of whole runs; return those runs (no equations allowed)."""
    pos = 0; sel = []
    for el, t in atoms(p):
        s, e = pos, pos + len(t); pos = e
        if e <= a or s >= b: continue
        assert el.tag == qn('w:r'), 'edit would delete an equation'
        if s < a:
            _, el = _split(el, a - s); t = t[a - s:]; s = a
        if e > b:
            el, _ = _split(el, b - s)
        sel.append(el)
    return sel

def _new_run(model, text, sup=False):
    r = OxmlElement('w:r')
    if model is not None and model.find(qn('w:rPr')) is not None:
        r.append(copy.deepcopy(model.find(qn('w:rPr'))))
    if sup:
        rpr = r.find(qn('w:rPr'))
        if rpr is None:
            rpr = OxmlElement('w:rPr'); r.insert(0, rpr)
        va = OxmlElement('w:vertAlign'); va.set(qn('w:val'), 'superscript'); rpr.append(va)
    t = OxmlElement('w:t'); t.text = text; t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    r.append(t)
    return r

def _delete(runs):
    d = _mark('w:del')
    runs[0].addprevious(d)
    for r in runs:
        for t in r.findall(qn('w:t')):
            t.tag = qn('w:delText')
        d.append(r)
    return d

def _insert_after(anchor, text, model, sup=False, before=False):
    ins = _mark('w:ins'); ins.append(_new_run(model, text, sup))
    (anchor.addprevious if before else anchor.addnext)(ins)
    return ins

def _model_at(p, k):
    """Run whose formatting a new run inserted at char k should copy."""
    pos = 0; last = None
    for el, t in atoms(p):
        if el.tag == qn('w:r'):
            if pos <= k < pos + len(t): return el
            if pos + len(t) <= k: last = el
        pos += len(t)
    return last

def _insert_at(p, k, text, model):
    pos = 0; ats = atoms(p)
    for el, t in ats:
        if pos == k:
            return _insert_after(el, text, model, before=True)
        if pos < k < pos + len(t):
            _, right = _split(el, k - pos)
            return _insert_after(right, text, model, before=True)
        pos += len(t)
    return _insert_after(ats[-1][0], text, model)

TOK = re.compile(r'\s+|[\w.−\-+%]+|.', re.S)

def replace(p, old, new):
    """Track-change `old` -> `new` inside paragraph p with a word-level diff."""
    txt = ptext(p)
    assert txt.count(old) == 1, f'{txt.count(old)} matches for: {old[:70]}'
    base = txt.index(old)
    a_t, b_t = TOK.findall(old), TOK.findall(new)
    ops = difflib.SequenceMatcher(a=a_t, b=b_t, autojunk=False).get_opcodes()
    # merge changes separated by short unchanged stretches (<= 3 tokens, no equation) into one phrase edit
    merged = []
    for op in ops:
        if merged and merged[-1][0] != 'equal' and op[0] != 'equal' :
            t, i1, _, j1, _ = merged[-1]; merged[-1] = ('replace', i1, op[2], j1, op[4]); continue
        merged.append(op)
    changed = True
    while changed:
        changed = False
        for k in range(1, len(merged) - 1):
            t, i1, i2, j1, j2 = merged[k]
            if t == 'equal' and merged[k-1][0] != 'equal' and merged[k+1][0] != 'equal' and i2 - i1 <= 3 \
                    and MATH not in ''.join(a_t[i1:i2]):
                merged[k-1:k+2] = [('replace', merged[k-1][1], merged[k+1][2], merged[k-1][3], merged[k+1][4])]
                changed = True; break
    ops = merged
    def off(i): return base + sum(len(x) for x in a_t[:i])
    for tag, i1, i2, j1, j2 in reversed(ops):
        if tag == 'equal': continue
        a, b = off(i1), off(i2); ins_txt = ''.join(b_t[j1:j2])
        model = _model_at(p, a)
        if b > a:
            d = _delete(_isolate(p, a, b))
            if ins_txt: _insert_after(d, ins_txt, d[0])
        else:   # pure insertion at a
            _insert_at(p, a, ins_txt, model)
    assert accepted_text(p) == txt.replace(old, new), (accepted_text(p), txt.replace(old, new))

def accepted_text(p):
    out = []
    for el in p.iter():
        if el.tag == qn('m:oMath') and el.getparent().tag != qn('m:oMathPara'):
            out.append(MATH)
        elif el.tag == qn('w:t') and not any(a.tag in (qn('m:oMath'), qn('w:del')) for a in el.iterancestors()):
            out.append(el.text or '')
    return ''.join(out)

def append(p, text, sup=False):
    last = [el for el, _ in atoms(p) if el.tag == qn('w:r')][-1]
    _insert_after(last, text, last, sup=sup)

def replace_all(p, new, sup=None):
    """Replace the whole text of a (table-cell) paragraph; optional superscript marker appended."""
    old = ptext(p)
    if old != new:
        replace(p, old, new)
    if sup:
        append(p, sup, sup=True)

def swap_drawing(old_run, new_run):
    """Tracked swap of a figure: old drawing run deleted, new drawing run inserted after it."""
    d = _mark('w:del'); old_run.addprevious(d); d.append(old_run)
    ins = _mark('w:ins'); ins.append(new_run); d.addnext(ins)
