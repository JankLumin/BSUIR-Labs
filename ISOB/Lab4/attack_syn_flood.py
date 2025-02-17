import asyncio

async def attack_connection(i: int):
    try:
        reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
        challenge = await asyncio.wait_for(reader.readline(), timeout=5)
        print(f"[SYN Flood {i}] Received: {challenge.decode().strip()}")
        await asyncio.sleep(10)
        writer.close()
        await writer.wait_closed()
    except Exception as e:
        print(f"[SYN Flood {i}] Ошибка: {e}")

async def main():
    tasks = [asyncio.create_task(attack_connection(i)) for i in range(20)]
    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
