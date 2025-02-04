import socket
import json
import base64
from server import simple_encrypt, simple_decrypt

USER_ID = "client1"
USER_KEY = b"client1secret"
HOST, PORT = "localhost", 12345


def send_request(action, data):
    req = {"action": action, "data": data}
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(json.dumps(req).encode())
    resp = s.recv(4096)
    s.close()
    return json.loads(resp.decode())


def client_flow():
    as_req = {"client_id": USER_ID}
    as_resp = send_request("AS", as_req)
    if "error" in as_resp:
        print("AS error:", as_resp["error"])
        return

    as_data_encrypted = base64.b64decode(as_resp["response"].encode())
    message_plain = simple_decrypt(USER_KEY, as_data_encrypted)
    as_msg = json.loads(message_plain.decode())
    session_key = base64.b64decode(as_msg["session_key"].encode())
    tgt_encrypted = as_msg["tgt"]
    print("Получен сеансовый ключ для TGS:", session_key.hex())

    service_id = "fileserver"
    authenticator = "dummy"
    tgs_req = {
        "tgt": tgt_encrypted,
        "service_id": service_id,
        "authenticator": base64.b64encode(authenticator.encode()).decode(),
    }
    tgs_resp = send_request("TGS", tgs_req)
    if "error" in tgs_resp:
        print("TGS error:", tgs_resp["error"])
        return

    tgs_data_encrypted = base64.b64decode(tgs_resp["response"].encode())
    tgs_message_plain = simple_decrypt(session_key, tgs_data_encrypted)
    tgs_msg = json.loads(tgs_message_plain.decode())
    service_session_key = base64.b64decode(tgs_msg["service_session_key"].encode())
    service_ticket = tgs_msg["service_ticket"]
    print("Получен сеансовый ключ для сервиса:", service_session_key.hex())

    service_authenticator = "dummy_service"
    svc_req = {
        "service_ticket": service_ticket,
        "authenticator": base64.b64encode(service_authenticator.encode()).decode(),
        "service_session_key": base64.b64encode(service_session_key).decode(),
    }
    svc_resp = send_request("SERVICE", svc_req)
    if "error" in svc_resp:
        print("SERVICE error:", svc_resp["error"])
        return

    print("Сервер подтвердил клиента:", svc_resp["client_id"])


if __name__ == "__main__":
    client_flow()
