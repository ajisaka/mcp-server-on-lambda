import logging

import uvicorn
from fastmcp import FastMCP
from fastmcp.server.dependencies import get_access_token
from pydantic import BaseModel

from mcp_server_on_lambda.auth import auth

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CalculationResult(BaseModel):
    value: int


mcp = FastMCP("MCP Demo", auth=auth)
app = mcp.http_app(
    path="/",
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


@mcp.tool
async def tool_user() -> str:
    access_token = get_access_token()
    return access_token.claims["google_token_info"]["email"]  # type: ignore


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
