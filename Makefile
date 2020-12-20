build:
	docker build . -t local/getlock

build-docs:
	docker build . -f docs.Dockerfile -t local/getlock-docs
