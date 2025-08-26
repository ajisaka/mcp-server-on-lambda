import logging

import uvicorn
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


@mcp.tool
def tool_add(x: int, y: int) -> CalculationResult:
    return CalculationResult(value=x + y)


@mcp.tool
def tool_sub(x: int, y: int) -> CalculationResult:
    return CalculationResult(value=x - y)


def main() -> None:
    uvicorn.run(mcp_app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
