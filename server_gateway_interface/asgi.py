import asyncio


async def app(scope, receive, send):
    assert scope["type"] == "http"

    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                [b"content-type", b"text/html"],
            ],
        }
    )
    await send({
        "type": "http.response.body",
        "body": b"hello world",
    })


# Start ASGI with the next command: uvicorn server_gateway_interface.asgi:app

# To check if the asgi works:
# curl http://localhost:8000

