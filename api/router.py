from aiohttp import web
import aiohttp_jinja2
import jinja2
import re
from telethon.client.downloads import MAX_CHUNK_SIZE
from config import Config

class Router:
    
    RANGE_REGEX = re.compile(r"bytes=([0-9]+)-")
    BLOCK_SIZE = MAX_CHUNK_SIZE
    ext_attachment = [".mp4", ]


    @aiohttp_jinja2.template('t.html')
    async def streamx(self, request):
      id_hex = request.match_info.get("id")
      serial = request.match_info.get("serial")
      id = int(id_hex)
      serialx = int(str(serial))
      namebv = await self.client.get_entity(serialx)
      chname = namebv.title
      message = await self.client.get_messages(serialx, ids=id)
      capx = message.message
      name = self.get_file_name(message)
      url = f"{Config.DOMAIN}/{id}/{serialx}"
      punc = '''!()[]|{};:'="\,<>./?@#$%^&*~'''
      for ele in name:
        if ele in punc:
          name = name.replace(ele, "")
      namex1 = name.replace('  ', '_').replace(' ', '_').replace('mkv', '').replace('mp4', '').replace('webm', '').replace('-', '_')
      return {'linkx' : url, 'titlexzz' : capx, 'serial' : chname, 'name' : namex1}

    async def hello(self, request):
        return web.Response(text="Bot By Sahil Nolia")

    async def Downloader(self, request):
        id_hex = request.match_info.get("id")
        chatx = request.match_info.get("serial")
        
        try:
            id = int(id_hex)
            chatz = int(chatx)
        except ValueError:
            return web.HTTPNotFound()
        
        message = await self.client.get_messages(chatz, ids=id)

        if not message or not message.file :
            return web.HTTPNotFound()
        
        offset = request.headers.get("Range", 0)

        if not isinstance(offset, int):
            matches = self.RANGE_REGEX.search(offset)
            if matches is None:
                return web.HTTPBadRequest()
            offset = matches.group(1)
            if not offset.isdigit():
                return web.HTTPBadRequest()
            offset = int(offset)

        file_size = message.file.size
        file_ext = message.file.ext
        download_skip = (offset // self.BLOCK_SIZE) * self.BLOCK_SIZE
        read_skip = offset - download_skip
        
        name = request.match_info.get("name") or self.get_file_name(message)

        if download_skip >= file_size:
            return web.HTTPRequestRangeNotSatisfiable()

        if read_skip > self.BLOCK_SIZE:
            return web.HTTPInternalServerError()

        resp = web.StreamResponse(
            headers={
                'Content-Type': message.file.mime_type, #'application/octet-stream',
                'Accept-Ranges': 'bytes',
                'Content-Range': f'bytes {offset}-{file_size}/{file_size}',
                "Content-Length": str(file_size),
                "Content-Disposition": f'attachment; filename={name}' if file_ext in self.ext_attachment else f'inline; filename={name}' ,
            },
            status = 206 if offset else 200,
        )
        await resp.prepare(request)

        cls = self.client.iter_download(message.media, offset=download_skip)

        async for part in cls:
            if len(part) < read_skip:
                read_skip -= len(part)
            elif read_skip:
                await resp.write(part[read_skip:])
                read_skip = 0
            else:
                await resp.write(part)
                
        return resp