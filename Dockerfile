FROM ghcr.io/astral-sh/uv:python3.12-bookworm AS builder

ARG APP_ROOT="/app"
WORKDIR "${APP_ROOT}"

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter

COPY pyproject.toml uv.lock ./
COPY src ./src

ENV UV_COMPILE_BYTECODE=1
ENV UV_NO_INSTALLER_METADATA=1
ENV UV_LINK_MODE=copy

RUN uv export > requirements.txt
RUN uv pip install -r requirements.txt --system

EXPOSE 8080
ENTRYPOINT ["python"]
