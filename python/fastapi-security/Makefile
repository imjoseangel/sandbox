.DEFAULT_GOAL:=help

PATH     := $(PATH):$(PWD)/bin
OS       := $(shell uname -s | tr '[:upper:]' '[:lower:]' | sed 's/darwin/apple-darwin/' | sed 's/linux/linux-gnu/')
ARCH     := $(shell uname -m)

.POSIX:

.PHONY: help
help:  ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

.PHONY: runuvi
runuvi: ## Run app with uvicorn
	$(info Make: Run app)
	@python -m uvicorn --app-dir app main:app --host 0.0.0.0 --port 8000

.PHONY: run
run: ## Run app
	$(info Make: Run app)
	@fastapi dev app/main.py
