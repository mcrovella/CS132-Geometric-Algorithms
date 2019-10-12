DOCNAME = book

SRCS = \
L0Introduction.ipynb \
L0Clickers.ipynb \
L1LinearEquations.ipynb \
L2RowReductions.ipynb \
L3VectorEquations.ipynb

# TEXS=$(SRCS:.ipynb=.tex)

TGTS=$(SRCS:.ipynb=.pdf)

############################## shouldn't need to change below this line

LATEX  = pdflatex

.SUFFIXES: .ipynb .tex .pdf

%.tex: %.ipynb
	jupyter nbconvert --to=latex --template=printviewlatex.tplx $<

%.pdf: %.tex
	$(LATEX) $<
	rm $*.out $*.log $*.aux
	/bin/rm -rf $*_files

topleveltarget: $(TGTS)

figures:
	jupyter nbconvert --to notebook --inplace --execute *.ipynb
	cp json/* ~/www/cs132-figures
	chmod a+r ~/www/cs132-figures/*










