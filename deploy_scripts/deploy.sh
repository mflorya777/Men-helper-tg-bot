#!/usr/bin/env bash


set -e
set -x
echo "ENV = $ENV"
echo "TARGET_HOST_NAME = $TARGET_HOST_NAME"
echo "IMAGE_NAME = $IMAGE_NAME"
echo "DEPLOY_DIRECTORY = $DEPLOY_DIRECTORY"

COMPOSE_FILE_DESTINATION=$DEPLOY_DIRECTORY/docker-compose.yaml

TMP_COMPOSE_FILE_NAME="docker-compose.to_deploy.yaml"

docker compose -f compose/docker-compose.yaml config > $TMP_COMPOSE_FILE_NAME

# Make directory
RUN_COMMAND="mkdir -p $DEPLOY_DIRECTORY"

ssh root@$TARGET_HOST_NAME $RUN_COMMAND

# Coopy compose file

scp $TMP_COMPOSE_FILE_NAME "root@$TARGET_HOST_NAME:$COMPOSE_FILE_DESTINATION"

# Authorize docker to pull image from gitea
ssh -t root@$TARGET_HOST_NAME docker login gitea.rzd.energy

ssh -t root@$TARGET_HOST_NAME  docker compose -f $COMPOSE_FILE_DESTINATION pull
ssh -t root@$TARGET_HOST_NAME  docker compose -f $COMPOSE_FILE_DESTINATION down
ssh -t root@$TARGET_HOST_NAME  docker compose -f $COMPOSE_FILE_DESTINATION up -d
