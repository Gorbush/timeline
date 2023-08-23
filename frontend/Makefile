PHONY: install build push

install:
	npm i

build:
	docker build . -t hulk66/timeline_fe:0.96-dev

build-prod:
	docker build . -t hulk66/timeline_fe:0.96

push-prod:	
	docker push hulk66/timeline_fe:0.96

dev:
	npm run serve
