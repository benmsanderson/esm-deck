from docx.oxml.ns import qn
M = '□'   # placeholder for an inline equation
def ptext(p):
    out = []
    for el in p.iter():
        if el.tag == qn('m:oMath'):
            out.append(M)
        elif el.tag == qn('w:t') and not any(a.tag == qn('m:oMath') for a in el.iterancestors()):
            out.append(el.text or '')
        elif el.tag == qn('w:tab'):
            out.append('\t')
    return ''.join(out)
