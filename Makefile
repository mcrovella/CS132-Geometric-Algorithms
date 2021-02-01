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

movefigures:
	(cd json; python generate-configs.py)
	scp json/Fig*json crovella@csa2.bu.edu:www/cs132-figures
	ssh crovella@csa2.bu.edu 'chmod a+r ~/www/cs132-figures/*'
	scp json/config*.json crovella@csa2.bu.edu:www/diagramar
	ssh crovella@csa2.bu.edu 'chmod a+r ~/www/diagramar/*'

movebook:
	jupyter-book build book
	scp -r book/_build/html crovella@csa2.bu.edu:www/cs132-book
	ssh crovella@csa2.bu.edu 'chmod -R a+r ~/www/cs132-book'







