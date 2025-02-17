import asyncio

async def proper_client():
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

        challenge = await asyncio.wait_for(reader.readline(), timeout=5)
        print(f"[Client] Received: {challenge.decode().strip()}")
        if challenge.decode().startswith("CHALLENGE"):
            token = challenge.decode().split()[1]
            writer.write(f"RESPONSE {token}\n".encode())
            await writer.drain()
            handshake_result = await reader.readline()
            print(f"[Client] Handshake result: {handshake_result.decode().strip()}")
        else:
            print("[Client] Нет handshake, защита отключена.")

        welcome = await reader.readline()
        print(f"[Client] {welcome.decode().strip()}")

        writer.write("PING\n".encode())
        await writer.drain()
        pong = await reader.readline()
        print(f"[Client] {pong.decode().strip()}")

        writer.write("quit\n".encode())
        await writer.drain()
        goodbye = await reader.readline()
        print(f"[Client] {goodbye.decode().strip()}")

        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"[Client] Ошибка: {e}")

if __name__ == '__main__':
    asyncio.run(proper_client())
