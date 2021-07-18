
version := $(shell git describe --tags --always --first-parent --abbrev=7 --dirty=.dirty)

test:
	pytest tests

docker: test
	docker build . -t 130966031144.dkr.ecr.eu-west-1.amazonaws.com/summer-capstone/export:$(version)

docker-push: docker
	docker push 130966031144.dkr.ecr.eu-west-1.amazonaws.com/summer-capstone/export:$(version)

deploy: docker-push
	cd infrastructure && terraform init && terraform apply