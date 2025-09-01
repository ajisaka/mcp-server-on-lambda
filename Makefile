STACK_NAME=mcp-server-on-lambda
SAM_CONFIG_FILE=samconfig.toml

.PHONY: dev
dev:
	uv run app

.PHONY: deploy
deploy: test
ifeq (,$(wildcard $(SAM_CONFIG_FILE)))
	$(eval DEPLOY_OPTS=--guided --stack-name $(STACK_NAME))
else
	$(eval DEPLOY_OPTS=)
endif
	echo "SAM_CONFIG_FILE=$(SAM_CONFIG_FILE)"
	echo "DEPLOY_OPTS=$(DEPLOY_OPTS)"
	sam build --use-container
	sam deploy $(DEPLOY_OPTS) --config-file $(SAM_CONFIG_FILE) \
		--no-confirm-changeset \
		--resolve-image-repos \
		--capabilities "CAPABILITY_IAM" "CAPABILITY_AUTO_EXPAND"

.PHONY: test
test: check
	uv run pre-commit run --all-files
	uv run cfn-lint template.yaml

.PHONY: check
check:
ifeq (,$(STACK_NAME))
	@echo 'STACK_NAME is not defined'
	false
endif

.PHONY: setup
setup:
	uv run pre-commit install

.PHONY: build-container
build-container:
	docker build --build-arg LAMBDA_TASK_ROOT=/lambda -t mcp-server-on-lambda .
