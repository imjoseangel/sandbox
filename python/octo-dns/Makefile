# Current version
# VERSION ?= 1.0.3

.DEFAULT_GOAL:=help

PATH  := $(PATH):$(PWD)/bin
OS    = $(shell uname -s | tr '[:upper:]' '[:lower:]')
ARCH  = $(shell uname -m | sed 's/x86_64/amd64/')
OSOPER   = $(shell uname -s | tr '[:upper:]' '[:lower:]' | sed 's/darwin/apple-darwin/' | sed 's/linux/linux-gnu/')
ARCHOPER = $(shell uname -m )

.PHONY: help reqs lint

help:  ## Display this help
		@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

all: reqs lint

.PHONY: reqs
reqs: ## Install Python requirements
		$(info Make: Python requirements)
		pip install --upgrade -r requirements.txt

.PHONY: lint
lint: ## Static Check
		$(info Make: Static Lint Check)
		pre-commit run --all-files

.PHONY: build
build: ## Build Docker Image
		$(info Make: Build Docker Image)
		docker buildx build --platform linux/amd64 -t imjoseangel/verify:latest .
