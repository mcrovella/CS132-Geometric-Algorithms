import sys

inVerbatim = 0
for line in sys.stdin:
    if ((line.find("\\begin{Verbatim}") > -1) or (line.find("\\begin{verbatim}") > -1)):
        inVerbatim = 1
        vblock = line
    elif inVerbatim:
        vblock = vblock + line
        if ((line.find('\\end{Verbatim}') > -1) or (line.find('\\end{verbatim}') > -1)):
            inVerbatim = 0
            # Things that we omit as verbatim: blocks containing
            # hide_code_in_slideshow
            # %matplotlib inline
            # IPython.core.display.HTML
            # %%html
            if ((vblock.find('hide\\PYZus{}code\\PYZus{}in\\PYZus{}slideshow') < 0) 
            and (vblock.find('\\PY{k}{matplotlib} \\PY{n}{inline}') < 0)
            and (vblock.find('IPython.core.display.HTML') < 0)
            and (vblock.find('\\PY{o}{\\PYZpc{}\\PYZpc{}}\\PY{k}{html}') < 0)):
                print vblock,
    else:
        print line,
