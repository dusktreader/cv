.ONESHELL:
.DEFAULT_GOAL:=help
SHELL:=/bin/bash

light:  ## Generate the light version of my cv
	uv run render --color=light --output=tucker-beck-cv--light.pdf

night:  ## Generate the night version of my cv
	uv run render --color=night --output=tucker-beck-cv--night.pdf

sizzle:  ## Generate the sizzle version of my cv
	uv run render --color=sizzle --output=tucker-beck-cv--sizzle.pdf

all: light night sizzle  ## Generate all versions of my cv

clean:  ## Clean up build artifacts and other junk
	@uv run pyclean . --debris

# Recipe stolen from: https://gist.github.com/prwhite/8168133?permalink_comment_id=4160123#gistcomment-4160123
help:  ## Show help message
	@awk 'BEGIN {FS = ": .*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+(\\:[$$()% 0-9a-zA-Z_-]+)*:.*?##/ { gsub(/\\:/,":", $$1); printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
