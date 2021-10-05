.PHONY: book figures

figures:
	jupyter nbconvert --to notebook --inplace --execute *.ipynb

book:
        # -v verbose
        # -all re-build all pages not just changed pages
        # -W make warning treated as errors
        # -n nitpick generate warnings for all missing links
        # --keep-going despite -W don't stop delay errors till the end
	jupyter-book build -v -n --keep-going .

pushbook:
	cp -r _build/html/* docs
	git add docs
	git commit -m 'book update'
	git push

movefigures:
	(cd json; python generate-configs.py)
	scp json/Fig*json crovella@csa2.bu.edu:www/cs132-figures
	ssh crovella@csa2.bu.edu 'chmod a+r ~/www/cs132-figures/*'
	scp json/config*.json crovella@csa2.bu.edu:www/diagramar
	ssh crovella@csa2.bu.edu 'chmod a+r ~/www/diagramar/*'

movebook:
	ssh crovella@csa2.bu.edu '/bin/rm -rf ~/www/cs132-text/spring-2022'
	scp -r _build/html crovella@csa2.bu.edu:www/cs132-text/spring-2022
	ssh crovella@csa2.bu.edu 'chmod -R a+rx ~/www/cs132-text/spring-2022'







