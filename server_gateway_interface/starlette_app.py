from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def homepage(request):
    return PlainTextResponse("hello world")


app = Starlette(
    routes=[
        Route("/", homepage),
    ],
)

# Start with the next command: uvicorn server_gateway_interface.starlette_app:app

# To check if the starlette works:
# curl http://localhost:8000
