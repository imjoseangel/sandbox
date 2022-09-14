# Current version
# VERSION ?= 1.0.4

.DEFAULT_GOAL:=help

PATH     := $(PATH):$(PWD)/bin
OS       := $(shell uname -s | tr '[:upper:]' '[:lower:]' | sed 's/darwin/apple-darwin/' | sed 's/linux/linux-gnu/')
ARCH     := $(shell uname -m)

.PHONY: help all check profile

help:  ## Display this help
		$(info Make: $@)
		$(info )
		@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "  \033[36m%-10s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

all: profile

check: ## Input check
		@[ "${scr}" ] || ( echo "\033[36mscr\033[0m is not set"; exit 1 )

profile: check ## Profiling
		$(info Make: $@)
		$(info )
		@python -m cProfile -s cumulative $(scr)
