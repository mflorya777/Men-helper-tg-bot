SHELL:=/bin/bash

APP_NAME := woman-tg-bot
APP_ROOT := src
REGISTRY_NAME = github.com
APP_TEST_IMAGE_NAME := $(APP_NAME)-$(shell git rev-parse HEAD)-test
APP_TEST_LOCAL_IMAGE_NAME := $(APP_NAME)-local-test
BASE_IMAGE_NAME := $(REGISTRY_NAME)/${APP_NAME}:base
ENV ?= local
DEPLOY_DIRECTORY = /opt/$(APP_NAME)
OS_TYPE = $(shell uname)

ifeq ($(ENV), local)
TARGET_HOST_NAME = $(shell hostname)
FILES_STORAGE_DIRECTORY = $(shell pwd)/files_storage_directory
else
TARGET_HOST_NAME = $(ENV)-$(APP_NAME)
FILES_STORAGE_DIRECTORY = $(DEPLOY_DIRECTORY)/files_storage_directory
endif

export ENV
export TARGET_HOST_NAME
export FILES_STORAGE_DIRECTORY
export DEPLOY_DIRECTORY
export DOCKER_DEFAULT_PLATFORM=linux/amd64

info:  ## Показать информацию о проекте
	@echo "********** Info **********"
	@echo "version =$(shell make version)" | awk '{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "full_image_name =$(shell make full_image_name)" | awk '{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "********** Makefile settings **********"
	@echo "OS_TYPE =$(OS_TYPE)" | awk '{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "TARGET_HOST_NAME =$(TARGET_HOST_NAME)" | awk '{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "ENV =$(ENV)" | awk '{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "APP_NAME =$(APP_NAME)" | awk '{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "APP_ROOT =$(APP_ROOT)" | awk '{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "APP_TEST_IMAGE_NAME =$(APP_TEST_IMAGE_NAME)" | awk '{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "APP_TEST_LOCAL_IMAGE_NAME =$(APP_TEST_LOCAL_IMAGE_NAME)" | awk '{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo "BASE_IMAGE_NAME =$(BASE_IMAGE_NAME)" | awk '{printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

help: info  ## Показать помощь (справку) и доступные команды
	@echo "********** Makefile usage help **********"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


define get_version
$(shell python3 -c "from $(APP_ROOT) import __version__; print(__version__)")
endef


define get_image_name
$(REGISTRY_NAME)/${APP_NAME}:$(call get_version)-$(ENV)
endef


tag:  ## Добавить соответствующий тег к git локально
	git tag $(call get_version)

version: ## Вывести текущую версию приложения
	@echo $(call get_version)


bump_version:  ## Bump version
ifeq ($(V),)
	@echo "Please enter new version V= , current version: $(call get_version)"
	exit 1
endif
ifneq ($(shell git status -s | grep -E '^\ M|^A' | wc -l | xargs), 0)
	@echo "Repo is not clean. Please commit and push changes first."
	exit 1
endif
	@echo "Bump version from $(call get_version) to $(V)"
ifeq ($(OS_TYPE), Linux)
	@sed -i 's/$(call get_version)/$(V)/g' $(APP_ROOT)/__init__.py
else
	@sed -i  '' -e 's/$(call get_version)/$(V)/g' $(APP_ROOT)/__init__.py
endif
	git add $(APP_ROOT)/__init__.py
	git commit -m "Bump version $(V)"
	git push

push_tag:  ## Отправить текущий тег на удаленный репозиторий
	git push origin $(call get_version)

remove_tag:
	git tag -d $(call version)
	git push --delete origin $(call version)

retag: remove_tag tag push_tag

full_image_name:  ## Получить имя образа в репозитории, включая: тег, версию, окружение
	@echo $(call get_image_name)

build_base_image:  ## Сбилдить базовый имедж
	eval `ssh-agent -s` \
	&& ssh-add ~/.ssh/id_rsa \
	&& DOCKER_BUILDKIT=1 \
	docker build \
		-f compose/base.Dockerfile \
		--platform $(DOCKER_DEFAULT_PLATFORM) \
		--ssh default=${SSH_AUTH_SOCK} \
		--target base \
		--add-host=gitea.rzd.energy:192.168.53.106 \
		-t $(BASE_IMAGE_NAME) . \
	&& ssh-agent -k

build_base_image:
	eval `ssh-agent -s`; ssh-add /mnt/c/Users/mih2303/.ssh/id_rsa; DOCKER_BUILDKIT=1 docker build -f compose/base.Dockerfile --platform linux/amd64 --ssh default= --target base --add-host=gitea.rzd.energy:192.168.53.106 -t github.com/woman-tg-bot:base .; ssh-agent -k


build_image:  ## Сбилдить имедж
	eval `ssh-agent -s` \
	&& ssh-add ~/.ssh/id_rsa \
	&& DOCKER_BUILDKIT=1 \
	docker build \
		-f compose/Dockerfile \
		--platform $(DOCKER_DEFAULT_PLATFORM) \
		--ssh default=${SSH_AUTH_SOCK} \
		--target production \
		--add-host=gitea.rzd.energy:192.168.53.106 \
		-t $(call get_image_name) . \
	&& ssh-agent -k

build_test_image:  ## Сбилдить тестовый имедж
	eval `ssh-agent -s` \
	&& ssh-add ~/.ssh/id_rsa \
	&& DOCKER_BUILDKIT=1 \
	docker build \
		-f compose/Dockerfile \
		--platform $(DOCKER_DEFAULT_PLATFORM) \
		--ssh default=${SSH_AUTH_SOCK} \
		--target dev \
		--add-host=gitea.rzd.energy:192.168.53.106 \
		-t $(APP_TEST_IMAGE_NEAME) . \
	&& ssh-agent -k

build_test_image_local:  ## Сбилдить тестовый имедж локально
	DOCKER_BUILDKIT=1 \
	docker build \
		-f compose/Dockerfile \
		--platform $(DOCKER_DEFAULT_PLATFORM) \
		--ssh default=~/.ssh/id_rsa \
		--target dev \
		--add-host=gitea.rzd.energy:192.168.53.106 \
		-t $(APP_TEST_LOCAL_IMAGE_NAME) .

push_image:
	docker push $(call get_image_name)

push_base_image:
	docker push $(BASE_IMAGE_NAME)

release: bump_version tag push_tag build_image push_image

rollout: build_image push_image deploy

deploy:
	export IMAGE_NAME=$(call get_image_name) && \
	deploy_scripts/deploy.sh

connect_to_target_host:
	ssh root@$(TARGET_HOST_NAME)

test:  ## Запустить тесты. Используем для GH Actions.
	docker run \
		-i \
		--env-file dev.env.example \
		$(APP_TEST_IMAGE_NAME) \
		pytest tests

test_local:  ## Запустить тесты локально. С использованием локального докер имеджа.
	docker run \
		-it \
		--env-file dev.env.example \
	    -v $(shell pwd):/opt/app \
		$(APP_TEST_LOCAL_IMAGE_NAME) \
		pytest tests

mypy:  ## Запустить mypy. Используем для GH Actions.
	docker run \
		--rm \
		-i \
		$(APP_TEST_IMAGE_NAME) \
		mypy .

mypy_local:  ## Запустить mypy локально. С использованием локального докер имеджа.
	docker run \
		-it \
	    -v $(shell pwd):/opt/app \
		$(APP_TEST_LOCAL_IMAGE_NAME) \
		mypy .


ruff_check:  ## Запустить ruff check. Используем для GH Actions.
	docker run \
		--rm \
		-i \
		$(APP_TEST_IMAGE_NAME) \
		ruff check

ruff_check_local:  ## Запустить ruff check локально. С использованием локального докер имеджа.
	docker run \
		-it \
	    -v $(shell pwd):/opt/app \
		$(APP_TEST_LOCAL_IMAGE_NAME) \
		ruff check .

ruff_format_check:  ## Запустить ruff format --check. Используем для GH Actions.
	docker run \
		--rm \
		-i \
		$(APP_TEST_IMAGE_NAME) \
		ruff format --check

ruff_format_check_local:  ## Запустить ruff format --check локально. С использованием локального докер имеджа.
	docker run \
		-it \
		--env-file dev.env.example \
	    -v $(shell pwd):/opt/app \
		$(APP_TEST_LOCAL_IMAGE_NAME) \
		ruff format --check

ruff_format_check_local_verbose:  ## Запустить ruff format --check локально. С использованием локального докер имеджа.
	docker run \
		-it \
		--env-file dev.env.example \
	    -v $(shell pwd):/opt/app \
		$(APP_TEST_LOCAL_IMAGE_NAME) \
		ruff format --check --verbose /opt/app

ruff_fix_local:  ## Пофиксить ошибки статического анализатора ruff.
	docker run \
		-it \
		--env-file dev.env.example \
	    -v $(shell pwd):/opt/app \
		$(APP_TEST_LOCAL_IMAGE_NAME) \
		ruff check --fix

ruff_format_fix_local:  ## Пофиксить ошибки форматирования с помощью ruff format.
	docker run \
		-it \
		--env-file dev.env.example \
	    -v $(shell pwd):/opt/app \
		$(APP_TEST_LOCAL_IMAGE_NAME) \
		ruff format

# Helpers
docker_bash:
	docker run \
		-it \
		--env-file $(ENV).env \
	    -v $(shell pwd):/opt/app \
		$(APP_TEST_LOCAL_IMAGE_NAME) \
		bash

# Запустить сервисы
run_stack:  ## Запустит все сервисы
	export IMAGE_NAME=$(call get_image_name) && \
	docker compose -f compose/docker-compose.$(ENV).yaml up -d

stop_stack:  ## Остановить все сервисы
	export IMAGE_NAME=$(call get_image_name) && \
	docker compose -f compose/docker-compose.$(ENV).yaml down

run_backend:  ## Запустить только backend API
	export IMAGE_NAME=$(call get_image_name) && \
	docker compose -f compose/docker-compose.$(ENV).yaml up -d woman-tg-bot

run_backend_local:  ## Запустить только backend API
	export IMAGE_NAME=$(APP_TEST_LOCAL_IMAGE_NAME) && \
	docker compose -f compose/docker-compose.$(ENV).yaml up -d woman-tg-bot

restart_stack: stop_stack run_stack  ## Перезапустить все сервисы

restart_backend_local: stop_stack run_backend_local

logs_backend:
	docker logs -f woman-tg-bot
