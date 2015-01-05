DOCNAME = book

SRCS = \
L1LinearEquations.ipynb

TEXS=$(SRCS:.ipynb=.tex)

TGTS=$(SRCS:.ipynb=.pdf)

PUBLISHDIR = /cs-pub/www-dir/faculty/crovella/restricted/pebook

############################## shouldn't need to change below this line

LATEX  = pdflatex

.SUFFIXES: .ipynb .tex .pdf

%.tex: %.ipynb
	/bin/rm -rf tmpFile
	ipython nbconvert $< --to latex
	mv $@ tmpFile
	python stripHiddenCode.py < tmpFile > $@
	rm tmpFile

%.pdf: %.tex
	$(LATEX) $<
	rm $*.out $*.log $*.aux

topleveltarget: $(TGTS)










