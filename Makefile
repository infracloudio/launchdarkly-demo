 
NAME:=sudhanshuinfracloud/ld-demo
TAG:=$(shell git log -1 --pretty=%h)
IMG:=${NAME}:${TAG}
LATEST:=${NAME}:latest
 
build:
	docker build -t ${IMG} .
	docker tag ${IMG} ${LATEST}

push:
	docker push ${NAME}

login:
	@docker login -u ${DOCKER_USER} -p ${DOCKER_PASS}