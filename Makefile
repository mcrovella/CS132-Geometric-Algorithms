.PHONY: book figures pushbook

figures:
figures: ## run all notebooks in order to regenerate all figures
	jupyter nbconvert --to notebook --inplace --execute *.ipynb

book:
book: ## compile the book but do not publish it
        # -v verbose
        # -all re-build all pages not just changed pages
        # -W make warning treated as errors
        # -n nitpick generate warnings for all missing links
        # --keep-going despite -W don't stop delay errors till the end
	jupyter-book build -v -n --keep-going .

pushbook:
pushbook: ## publish the last compiled book
	cp -r _build/html/* docs
	git add docs
	git commit -m 'book update'
	git push

help:
# http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html
	@grep -E '^[a-zA-Z0-9_%/-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

movefigures:
movefigures: ## transfer all the figures over to csa2
	(cd json; python generate-configs.py)
	scp json/Fig*json crovella@csa2.bu.edu:www/cs132-figures
	ssh crovella@csa2.bu.edu 'chmod a+r ~/www/cs132-figures/*'
	scp json/config*.json crovella@csa2.bu.edu:www/diagramar
	ssh crovella@csa2.bu.edu 'chmod a+r ~/www/diagramar/*'

movebook:
movebook: ## transfer the book over to csa2
	ssh crovella@csa2.bu.edu '/bin/rm -rf ~/www/cs132-text/spring-2022'
	scp -r _build/html crovella@csa2.bu.edu:www/cs132-text/spring-2022
	ssh crovella@csa2.bu.edu 'chmod -R a+rx ~/www/cs132-text/spring-2022'







