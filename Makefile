SHELL := /bin/bash

include Makefile.variables

.PHONY: help
help:
	@echo "Usage:	make COMMAND"
	@echo ""
	@echo "		Commands:"
	@echo "			docker_build			Build an image from a Dockerfile"
	@echo "			docker_build_dev		Build an image running under DEV mode"


.PHONY: docker_build
docker_build:
	@echo "Makefile-------> $(DOCKER_BUILD) -t $(PROD_IMAGE_NAME) -f $(DOCKERFILE_PROD) ."
	@echo "Coming Soon..."

.PHONY: docker_build_env
docker_build_dev:
	@echo "Makefile-------> $(DOCKER_BUILD) -t $(DEV_IMAGE_NAME) -f $(DOCKERFILE_DEV) ."
	$(DOCKER_BUILD) -t $(DEV_IMAGE_NAME) -f $(DOCKERFILE_DEV) .

