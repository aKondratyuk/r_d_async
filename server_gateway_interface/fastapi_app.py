from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def hello_wold() -> dict[str, str]:
    return {"message": "hello world"}

# Start with the next command: uvicorn server_gateway_interface.fastapi_app:app

# To check if the fastapi works:
# curl http://localhost:8000
