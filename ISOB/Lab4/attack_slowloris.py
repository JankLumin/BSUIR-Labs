import asyncio

async def slowloris_attack():
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
        challenge = await asyncio.wait_for(reader.readline(), timeout=5)
        print(f"[Slowloris] Received: {challenge.decode().strip()}")
        parts = challenge.decode().strip().split()
        if len(parts) != 2 or parts[0] != "CHALLENGE":
            print("[Slowloris] Неверный формат challenge.")
            writer.close()
            await writer.wait_closed()
            return
        token = parts[1]
        response = f"RESPONSE {token}\n"
        print("[Slowloris] Отправляем ответ медленно...")
        for ch in response:
            writer.write(ch.encode())
            await writer.drain()
            await asyncio.sleep(1)
        handshake_result = await reader.readline()
        print(f"[Slowloris] Handshake result: {handshake_result.decode().strip()}")
        await asyncio.sleep(10)
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"[Slowloris] Ошибка: {e}")

if __name__ == '__main__':
    asyncio.run(slowloris_attack())
