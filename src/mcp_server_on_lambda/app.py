import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from fastmcp import FastMCP
from mangum import Mangum
from pydantic import BaseModel

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CalculationResult(BaseModel):
    value: int


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


app: FastAPI
if __name__ == "__main__":
    print("Running in local mode")
    app = FastAPI(lifespan=combined_lifespan)
else:
    print("Runnning in AWS Lambda mode")
    app = FastAPI()


mcp = FastMCP("MCP Demo")
mcp_app = mcp.http_app(
    path="/mcp",
    json_response=True,
    stateless_http=True,
    transport="streamable-http",
)


@mcp.tool
def tool_add(x: int, y: int) -> CalculationResult:
    return CalculationResult(value=x + y)


@mcp.tool
def tool_sub(x: int, y: int) -> CalculationResult:
    return CalculationResult(value=x - y)


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)


# <HOST>/mcp/mcp
app.mount("/mcp", mcp_app)

lambda_handler = Mangum(app)


if __name__ == "__main__":
    main()
