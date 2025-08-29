import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastmcp import FastMCP
from pydantic import BaseModel

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CalculationResult(BaseModel):
    value: int


mcp = FastMCP("MCP Demo")
mcp_app = mcp.http_app(
    path="/mcp",
    json_response=True,
    stateless_http=True,
    transport="streamable-http",
)


# https://gofastmcp.com/integrations/fastapi#combining-lifespans
@asynccontextmanager
async def app_lifespan(app: FastAPI):  # type: ignore
    logger.info("Starting up the app...")
    yield
    logger.info("Shutting down the app...")


@asynccontextmanager
async def combined_lifespan(app: FastAPI):  # type: ignore
    async with app_lifespan(app):
        async with mcp_app.lifespan(app):  # type: ignore
            yield


app = FastAPI(lifespan=combined_lifespan)


@app.get("/")
def app_root() -> dict:
    return {"message": "Hello World"}


@app.get("/answer")
def app_answer() -> int:
    return 42


@mcp.tool
def tool_add(x: int, y: int) -> CalculationResult:
    return CalculationResult(value=x + y)


@mcp.tool
def tool_sub(x: int, y: int) -> CalculationResult:
    return CalculationResult(value=x - y)


app.mount("/mcp", mcp_app)


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
