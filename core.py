import asyncio
from random import random

TOPICS = list()

async def node_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    print("node handler called")

    data = await reader.read(1024)

    if not data:
        print("node name corrupted")
        return

    print("name: ", data.decode("utf-8"))

async def topic_handler(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
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

        if not data:
            break

        msg = data.decode("utf-8")
        print(msg)

def main():
    
    loop = asyncio.get_event_loop()
    node = asyncio.start_server(node_handler, host="127.0.0.1", port=5000, loop=loop)
    topic = asyncio.start_server(topic_handler, host="127.0.0.1", port=5001, loop=loop)
    topic_server = loop.run_until_complete(topic)
    node_server = loop.run_until_complete(node)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        print("Closing")
        node_server.close()
        topic_server.close()
        loop.run_until_complete(node_server.wait_closed())
        loop.run_until_complete(topic_server.wait_closed())
        loop.close()

if __name__ == "__main__":
    print("server running")
    main()