
version := $(shell git describe --tags --always --first-parent --abbrev=7 --dirty=.dirty)
dirs := preprocessor ingestion cleanup normalize sequence-mapper omics-parser-dynamic hyft-extractor

test:
	go test ./...

docker-push:
	$(foreach directory, $(dirs), (cd $(directory) && make docker-push);)

deploy-beta: docker-push
	cd resources/biostrand-1-beta && terraform init && terraform apply