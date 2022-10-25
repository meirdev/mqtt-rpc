from app import app


@app.task
def hello() -> str:
    return "hello!"


@app.task
def sum(a, b) -> int:
    return a + b
