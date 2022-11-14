# Common Docker and docker-compose commands
- https://docs.docker.com/engine/reference/commandline/compose_restart/

## Start the container stack and run in the background
- docker-compose up -d
- docker start CONTAINER_ID

## Restart the container, -t 0 says not to wait
- docker-compose restart -t 0

## Stop the container stack
- docker-compose down
- docker stop CONTAINER_ID

## List running containers
- docker ps

## List all the docker containers
- docker container ls 
- docker-compose ps

## List all the images
- docker image ls
- docker-compose images

## Open a bash shell in the container
- docker exec -it CONTAINER_ID bash
- docker exec -it CONTAINER_NAME bash

## Show stack logs
- docker-compose logs
