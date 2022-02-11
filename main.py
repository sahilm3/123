import api
import os
from aiohttp import web
import aiohttp_jinja2
import jinja2

hostx = os.getcwd()
server = api.Client()

async def main():
    app = web.Application()
    aiohttp_jinja2.setup(app,
    loader=jinja2.FileSystemLoader(hostx + '/views'))
    app.add_routes(
        [
            web.get('/', server.hello),
            web.get('/favicon.ico', server.hello),
            web.get('/{id}/{serial}/{name}', server.Downloader),
            web.get('/{id}/{serial}', server.Downloader),
            web.get('/{id}/sahil/stream/{serial}', server.streamx),
        ]
    )
    return app

if __name__ == "__main__":
    web.run_app(main())