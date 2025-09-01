import logging
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_http_request
from pydantic import BaseModel
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CalculationResult(BaseModel):
    value: int


class TestData(BaseModel):
    data: str


mcp = FastMCP("MCP Demo")
mcp_app = mcp.http_app(
    path="/mcp",
    json_response=True,
    stateless_http=True,
    transport="streamable-http",
)


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):  # type: ignore
        header = request.headers.get("Authorization")
        if header is None:
            raise HTTPException(status_code=401, detail="Unauthorized")
        request.state.test_data = header
        return await call_next(request)


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


@mcp.tool
def tool_test_data() -> TestData:
    request = get_http_request()
    return TestData(data=request.state.test_data)  # type: ignore


app.mount("/mcp", mcp_app)
app.add_middleware(AuthMiddleware)


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
