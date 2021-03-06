up:
	docker run --rm -d --name getlock-front \
		--network host \
		-v $$(pwd):/app \
		-w /app \
		--user 1000 \
		node:14-alpine sleep infinity

run:
	docker exec -ti --user 1000 getlock-front \
		npx ember serve

exec:
	docker exec -ti --user 1000 getlock-front \
		/bin/ash

down:
	docker stop getlock-front
