import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel


class CalculationResult(BaseModel):
    value: int


app = FastAPI(title="API Demo")


@app.get("/")
def api_root() -> bool:
    return True


@app.get("/add", response_model=CalculationResult)
def api_add(x: int, y: int) -> CalculationResult:
    return CalculationResult(value=x + y)


@app.get("/sub", response_model=CalculationResult)
def api_sub(x: int, y: int) -> CalculationResult:
    return CalculationResult(value=x - y)


def main() -> None:
    uvicorn.run(app, host="0.0.0.0", port=8080)


if __name__ == "__main__":
    main()
