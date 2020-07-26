import asyncio
from random import random

async def handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print("handler called")

    data = await reader.read(1024)

    if not data:
        return

    peername = writer.get_extra_info('peername')
    header = data.decode("utf-8")

    print("received: {} from {}".format(header, peername))

    header_info = header.split()

    if len(header_info) != 3:
        writer.write("0".encode("utf-8"))
        print("header corrupted")
        return

    topic_name = header_info[0]
    datatype = header_info[1]
    queue_size = header_info[2]

    writer.write("1".encode("utf-8"))

    while True:
        data = await reader.read(1024)
        msg = data.decode("utf-8")
        print(msg)

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