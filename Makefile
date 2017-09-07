.PHONY: clean-pyc clean-build

init:
		pip3 install -r requirements.txt

save-dependencies:
		pip3 freeze > requirements.txt

test:
		python3 setup.py test

clean-pyc:
		find . -name \*.pyc -delete

build-docker:
	docker build -t cyrptocoin_mixer .

run-docker:
	docker run -it -p 80:5000 cyrptocoin_mixer
