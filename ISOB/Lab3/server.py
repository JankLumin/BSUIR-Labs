import os
import json
import base64
import socketserver


def simple_encrypt(key: bytes, message: bytes) -> bytes:
    rep = (key * ((len(message) // len(key)) + 1))[:len(message)]
    return bytes(a ^ b for a, b in zip(message, rep))


def simple_decrypt(key: bytes, ciphertext: bytes) -> bytes:
    return simple_encrypt(key, ciphertext)


USER_SECRETS = {"client1": b"client1secret"}
AS_TGS_KEY = b"as_tgs_shared"
TGS_SERVICE_KEY = b"tgs_service_shared"


def generate_session_key() -> bytes:
    return os.urandom(16)


def as_process_authentication_request(client_id: str) -> bytes:
    if client_id not in USER_SECRETS:
        raise Exception("Unknown client")
    session_key = generate_session_key()
    tgt_plain = client_id.encode() + b"::" + session_key
    tgt_encrypted = simple_encrypt(AS_TGS_KEY, tgt_plain)
    msg = {
        "session_key": base64.b64encode(session_key).decode(),
        "tgt": base64.b64encode(tgt_encrypted).decode(),
    }
    message_plain = json.dumps(msg).encode()
    client_key = USER_SECRETS[client_id]
    message_encrypted = simple_encrypt(client_key, message_plain)
    print(f"[AS] Для клиента {client_id}:")
    print(f"     session_key = {session_key.hex()}")
    print(f"     TGT_plain    = {tgt_plain}")
    return message_encrypted


def tgs_process_service_request(
    tgt_encrypted_b64: str, service_id: str, authenticator_encrypted_b64: str
) -> bytes:
    tgt_encrypted = base64.b64decode(tgt_encrypted_b64.encode())
    tgt_plain = simple_decrypt(AS_TGS_KEY, tgt_encrypted)
    try:
        client_id_bytes, session_key = tgt_plain.split(b"::", 1)
    except Exception as e:
        raise Exception("Invalid TGT format") from e
    client_id = client_id_bytes.decode()
    print(f"[TGS] Извлечён client_id: {client_id}")
    print(f"[TGS] Извлечён session_key (из TGT) = {session_key.hex()}")
    service_session_key = generate_session_key()
    service_ticket_plain = json.dumps({
        "client_id": client_id,
        "service_session_key": base64.b64encode(service_session_key).decode()
    }).encode()
    service_ticket_encrypted = simple_encrypt(TGS_SERVICE_KEY, service_ticket_plain)
    msg = {
        "service_session_key": base64.b64encode(service_session_key).decode(),
        "service_ticket": base64.b64encode(service_ticket_encrypted).decode(),
    }
    message_plain = json.dumps(msg).encode()
    message_encrypted = simple_encrypt(session_key, message_plain)
    print(f"[TGS] Для сервиса {service_id}:")
    print(f"     service_session_key = {service_session_key.hex()}")
    print(f"     service_ticket_plain = {service_ticket_plain}")
    return message_encrypted


def service_process_client_request(
    service_ticket_encrypted_b64: str, authenticator_encrypted_b64: str, service_session_key_b64: str
) -> str:
    service_ticket_encrypted = base64.b64decode(service_ticket_encrypted_b64.encode())
    service_session_key = base64.b64decode(service_session_key_b64.encode())
    service_ticket_plain = simple_decrypt(TGS_SERVICE_KEY, service_ticket_encrypted)
    try:
        data = json.loads(service_ticket_plain.decode())
    except Exception as e:
        raise Exception("Invalid service ticket format") from e
    client_id = data.get("client_id")
    ticket_service_session_key_b64 = data.get("service_session_key")
    if not client_id or not ticket_service_session_key_b64:
        raise Exception("Invalid service ticket content")
    ticket_service_session_key = base64.b64decode(ticket_service_session_key_b64.encode())
    if ticket_service_session_key != service_session_key:
        raise Exception("Invalid service session key!")
    print(f"[SERVICE] Подтверждён client_id: {client_id}")
    return client_id


class KerberosRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(4096)
        if not data:
            return

        req = json.loads(data.decode())
        action = req.get("action")
        payload = req.get("data")
        resp = {}

        try:
            if action == "AS":
                client_id = payload["client_id"]
                result = as_process_authentication_request(client_id)
                resp["response"] = base64.b64encode(result).decode()
            elif action == "TGS":
                tgt = payload["tgt"]
                service_id = payload["service_id"]
                authenticator = payload["authenticator"]
                result = tgs_process_service_request(tgt, service_id, authenticator)
                resp["response"] = base64.b64encode(result).decode()
            elif action == "SERVICE":
                service_ticket = payload["service_ticket"]
                authenticator = payload["authenticator"]
                service_session_key = payload["service_session_key"]
                client_id = service_process_client_request(service_ticket, authenticator, service_session_key)
                resp["client_id"] = client_id
            else:
                resp["error"] = "Unknown action"
        except Exception as e:
            resp["error"] = str(e)
            print(f"[ERROR] При обработке {action}: {e}")

        self.request.sendall(json.dumps(resp).encode())


if __name__ == "__main__":
    HOST, PORT = "localhost", 12345
    server = socketserver.ThreadingTCPServer((HOST, PORT), KerberosRequestHandler)
    print(f"Kerberos-сервер запущен на {HOST}:{PORT}")
    server.serve_forever()
