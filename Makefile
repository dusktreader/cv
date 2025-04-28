.ONESHELL:
.DEFAULT_GOAL:=build
SHELL:=/bin/bash

build: build/json build/markdown  ## Build all the things

build/json:  ## Build the json file for the webpage
	uv run cv build json

build/markdown:  ## Build the README.md
	uv run cv build markdown

watch:  ## Watch for file changes and automatically generate and reload the cv
	@uv run cv watch --debug

clean:  ## Clean up build artifacts and other junk
	@uv run pyclean . --debris

# Recipe stolen from: https://gist.github.com/prwhite/8168133?permalink_comment_id=4160123#gistcomment-4160123
help:  ## Show help message
	@awk 'BEGIN {FS = ": .*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+(\\:[$$()% 0-9a-zA-Z_-]+)*:.*?##/ { gsub(/\\:/,":", $$1); printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
