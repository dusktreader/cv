.ONESHELL:
.DEFAULT_GOAL:=light
SHELL:=/bin/bash

light:  ## Generate the light version of my cv
	uv run cv resume

blue:  ## Generate the light version of my cv
	uv run cv resume --color=blue

night:  ## Generate the night version of my cv
	uv run cv resume --color=night

bold:  ## Generate the bold version of my cv
	uv run cv resume --color=bold

all: light night bold blue  ## Generate all versions of my cv

watch:  ## Watch for file changes and automatically generate and reload the cv
	@uv run cv watch

clean:  ## Clean up build artifacts and other junk
	@uv run pyclean . --debris
	@rm -f *.html
	@rm -f *.pdf

# Recipe stolen from: https://gist.github.com/prwhite/8168133?permalink_comment_id=4160123#gistcomment-4160123
help:  ## Show help message
	@awk 'BEGIN {FS = ": .*##"; printf "\nUsage:\n  make \033[36m\033[0m\n"} /^[$$()% 0-9a-zA-Z_-]+(\\:[$$()% 0-9a-zA-Z_-]+)*:.*?##/ { gsub(/\\:/,":", $$1); printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2 } /^##@/ { printf "\n\033[1m%s\033[0m\n", substr($$0, 5) } ' $(MAKEFILE_LIST)
