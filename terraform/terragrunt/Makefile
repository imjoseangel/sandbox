.DEFAULT_GOAL:=help

PATH     := $(PATH):$(PWD)/bin
OS       := $(shell uname -s | tr '[:upper:]' '[:lower:]' | sed 's/darwin/apple-darwin/' | sed 's/linux/linux-gnu/')
ARCH     := $(shell uname -m)

.POSIX:

.PHONY: all
all: check validate

.PHONY: help
help:  ## Display this help
		@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: validate
validate:
	terragrunt run-all plan

.PHONY: plan
plan: check ## Plan Terraform
	terragrunt run-all plan --terragrunt-working-dir=envs/$(env)

.PHONY: check
check:
	$(info Make: Check Variables)
	@[ "${env}" ] || ( echo "\033[36menv\033[0m is not set"; exit 1 )
