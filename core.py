import asyncio
from random import random

async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print("handler called")
    while True:
        data = await reader.read(1024)

        if not data:
            break

        peername = writer.get_extra_info('peername')
        msg = data.decode("utf-8")

        print("received: {} from {}".format(msg, peername))

def main():
    
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(handler, host="127.0.0.1", port=5001, loop=loop)
    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        server.close()
        print("closing")
        loop.run_until_complete(server.wait_closed())
        loop.close()

if __name__ == "__main__":
    print("server running")
    main()