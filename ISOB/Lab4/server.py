import asyncio
import random
import string
import time
import argparse
import logging

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")

parser = argparse.ArgumentParser(
    description="Запуск защищённого сервера. По умолчанию защита включена."
)
parser.add_argument(
    "--disable-protection",
    action="store_true",
    help="Запустить сервер без защитных механизмов.",
)
args = parser.parse_args()

PROTECTION_ENABLED = not args.disable_protection

MAX_HALF_OPEN_CONNECTIONS = 50
half_open_connections = set()

ACK_THRESHOLD = 3
ACK_WINDOW = 1


async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
    peername = writer.get_extra_info("peername")
    logging.info(f"Новое соединение от {peername}")

    if PROTECTION_ENABLED and len(half_open_connections) >= MAX_HALF_OPEN_CONNECTIONS:
        writer.write("Server busy. Try again later.\n".encode())
        await writer.drain()
        writer.close()
        await writer.wait_closed()
        logging.warning(
            f"Отклонено соединение от {peername} (слишком много незавершённых handshake). Возможная SYN Flood атака."
        )
        return

    handshake_success = False
    token = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

    if PROTECTION_ENABLED:
        try:
            half_open_connections.add(peername)
            writer.write(f"CHALLENGE {token}\n".encode())
            await writer.drain()
            response = await asyncio.wait_for(reader.readline(), timeout=5.0)
            response = response.decode().strip()
            if response == f"RESPONSE {token}":
                handshake_success = True
                writer.write("HANDSHAKE SUCCESS\n".encode())
                await writer.drain()
                logging.info(f"Успешный handshake с {peername}")
            else:
                writer.write("HANDSHAKE FAILED\n".encode())
                await writer.drain()
                logging.warning(
                    f"Неверный ответ от {peername}: {response}. Возможная попытка атаки."
                )
        except asyncio.TimeoutError:
            writer.write("HANDSHAKE TIMEOUT\n".encode())
            await writer.drain()
            logging.warning(
                f"Handshake timeout для {peername}. Возможная Slowloris или SYN Flood атака."
            )
        finally:
            half_open_connections.discard(peername)
    else:
        handshake_success = True
        writer.write("Protection disabled. Connection accepted.\n".encode())
        await writer.drain()
        logging.info(
            f"Защита отключена: соединение от {peername} принято без handshake"
        )

    if not handshake_success:
        writer.close()
        await writer.wait_closed()
        logging.info(f"Соединение с {peername} закрыто из-за неуспешного handshake.")
        return

    writer.write(
        "Добро пожаловать на защищённый сервер.\n"
        "Доступные команды: PING, ACK, quit\n".encode()
    )
    await writer.drain()

    ack_count = 0
    ack_window_start = time.monotonic()

    while True:
        try:
            data = await asyncio.wait_for(reader.readline(), timeout=30.0)
        except asyncio.TimeoutError:
            writer.write("Connection timed out due to inactivity.\n".encode())
            await writer.drain()
            logging.info(
                f"Соединение с {peername} разорвано из-за таймаута бездействия."
            )
            break

        if not data:
            break

        message = data.decode().strip()

        if message.upper() == "ACK":
            current_time = time.monotonic()
            if current_time - ack_window_start > ACK_WINDOW:
                ack_count = 0
                ack_window_start = current_time
            ack_count += 1
            if ack_count > ACK_THRESHOLD:
                writer.write("ACK flood detected. Connection dropped.\n".encode())
                await writer.drain()
                logging.warning(
                    f"ACK flood detected от {peername} (count: {ack_count}). Соединение разорвано."
                )
                break
            writer.write("ACK received.\n".encode())
            await writer.drain()
            continue

        if message.lower() == "quit":
            writer.write("Goodbye!\n".encode())
            await writer.drain()
            break
        elif message.upper() == "PING":
            writer.write("PONG\n".encode())
            await writer.drain()
        else:
            writer.write(f"Unknown command: {message}\n".encode())
            await writer.drain()

    writer.close()
    await writer.wait_closed()
    logging.info(f"Соединение с {peername} закрыто.")


async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 8888)
    addrs = ", ".join(str(sock.getsockname()) for sock in server.sockets)
    mode = "включена" if PROTECTION_ENABLED else "отключена"
    logging.info(f"Сервер запущен на {addrs} с защитой {mode}")
    async with server:
        await server.serve_forever()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Сервер остановлен.")
