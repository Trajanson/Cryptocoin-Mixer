.PHONY: clean-pyc clean-build

init:
		pip install -r requirements.txt

save-dependencies:
		pip freeze > requirements.txt

test:
		python setup.py test

clean-pyc:
		find . -name \*.pyc -delete
