build:
	docker build . -t local/getlock

run: build
	docker run --rm -ti --network host local/getlock

build-docs:
	docker build . -f docs.Dockerfile -t local/getlock-docs
