.PHONY: clean-pyc clean-build

init:
		pip install -r requirements.txt

save-dependencies:
		pip freeze > requirements.txt

test:
		python setup.py test

clean-pyc:
		find . -name \*.pyc -delete

build-docker:
	docker build -t cyrptocoin_mixer .

run-docker:
	docker run -it cyrptocoin_mixer
