import asyncio


async def attack_ack_flood(i: int):
    try:
        reader, writer = await asyncio.open_connection("127.0.0.1", 8888)
        challenge = await asyncio.wait_for(reader.readline(), timeout=5)
        text = challenge.decode().strip()
        if text.startswith("CHALLENGE"):
            parts = text.split()
            token = parts[1] if len(parts) > 1 else ""
            writer.write(f"RESPONSE {token}\n".encode())
            await writer.drain()
            handshake_result = await reader.readline()
            print(f"[ACK Flood {i}] Handshake: {handshake_result.decode().strip()}")
        else:
            print(f"[ACK Flood {i}] Received: {text}")

        for j in range(10000):
            writer.write("ACK\n".encode())
            await writer.drain()
            await asyncio.sleep(0.01)
            try:
                resp = await asyncio.wait_for(reader.readline(), timeout=1)
                if not resp:
                    break
                print(f"[ACK Flood {i}] Response: {resp.decode().strip()}")
            except asyncio.TimeoutError:
                break
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"[ACK Flood {i}] Ошибка: {e}")


async def main():
    tasks = [asyncio.create_task(attack_ack_flood(i)) for i in range(10)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
