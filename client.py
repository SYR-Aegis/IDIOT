import asyncio

async def run_client(host: str, port: int):

    reader, writer = await asyncio.open_connection(host=host, port=port)

    print("Connected")

    msg = "test int 10"

    if not msg:
        return

    payload = msg.encode("utf-8")
    writer.write(payload)

    await writer.drain()

    print("sent: {}".format(msg))
    print("waiting request...")

    response = await reader.read(1024)
    response_str = response.decode("utf-8")

    while True:
        try:
            if response_str == "0":
                print("connection failed")
            elif response_str == "1":
                print("connceted")
                writer.write("hello".encode("utf-8"))
            else:
                print("debug it man!")
        except KeyboardInterrupt:
            break

    print("closing connection ...")
    writer.close()

def main():
    loop = asyncio.get_event_loop()
    client = loop.run_until_complete(run_client(host="127.0.0.1", port=5001))

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        client.close()
        loop.run_until_complete(client)
        loop.close()

if __name__ == "__main__":
    main()