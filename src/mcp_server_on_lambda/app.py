import logging

import uvicorn
from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class CalculationResult(BaseModel):
    value: int


app = FastAPI()


@app.get("/add", operation_id="add")
def tool_add(x: int, y: int) -> CalculationResult:
    return CalculationResult(value=x + y)


@app.get("/sub", operation_id="sub")
def tool_sub(x: int, y: int) -> CalculationResult:
    return CalculationResult(value=x - y)


mcp_app = FastApiMCP(app)
mcp_app.mount_http()


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
