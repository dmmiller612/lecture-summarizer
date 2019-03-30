docker-build:
	docker build -t local-summary -f Dockerfile ./

docker-test:
	docker build -t local-summary -f Dockerfile ./
	docker run --rm -it local-summary:latest python ./test/tests.py

docker-run:
	docker run --rm -it -p 5000:5000 local-summary:latest

docker-build-run:
	docker build -t local-summary -f Dockerfile ./
	docker run --rm -it -p 5000:5000 local-summary:latest