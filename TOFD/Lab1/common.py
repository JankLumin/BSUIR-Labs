from __future__ import annotations

import json
import os
import time
from typing import Optional, Literal, Any

import base58
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.signature import Signature
from solana.rpc.api import Client
from solana.rpc.types import TxOpts

LAMPORTS_PER_SOL = 1_000_000_000
Commitment = Literal["processed", "confirmed", "finalized"]

DEFAULT_COMMITMENT: Commitment = "confirmed"
DEFAULT_TIMEOUT: float = 60.0
DEFAULT_POLL: float = 0.3
DEFAULT_SKIP_PREFLIGHT: bool = False
DEFAULT_MAX_RETRIES: Optional[int] = None


def get_client(url: Optional[str] = None) -> Client:
    u = url or os.getenv("SOLANA_URL") or "http://127.0.0.1:8899"
    return Client(u)


def save_keypair(kp: Keypair, path: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    data = {
        "public_key": str(kp.pubkey()),
        "secret_key_b58": base58.b58encode(bytes(kp)).decode(),
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved keypair → {path}\nPublic Key: {kp.pubkey()}")


def load_keypair(path: str) -> Keypair:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    secret = base58.b58decode(data["secret_key_b58"])
    return Keypair.from_bytes(secret)


def pubkey_from_str(addr: str) -> Pubkey:
    return Pubkey.from_string(addr)


def resolve_pubkey(value: str) -> Pubkey:
    if os.path.exists(value) and os.path.isfile(value):
        try:
            with open(value, "r", encoding="utf-8") as f:
                data = json.load(f)
            if isinstance(data, dict) and "public_key" in data:
                return Pubkey.from_string(data["public_key"])
        except Exception:
            pass
        try:
            kp = load_keypair(value)
            return kp.pubkey()
        except Exception as e:
            raise ValueError(
                f"Failed to read public key from file '{value}': {e}"
            ) from e
    return Pubkey.from_string(value)


def _as_dict(resp: Any) -> Optional[dict]:
    if isinstance(resp, dict):
        return resp
    try:
        to_json = getattr(resp, "to_json", None)
        if callable(to_json):
            j = to_json()
            if isinstance(j, dict):
                return j
            if isinstance(j, str):
                try:
                    return json.loads(j)
                except Exception:
                    return None
    except Exception:
        pass
    return None


def extract_sig(resp: Any) -> str:
    for attr in ("value", "result"):
        v = getattr(resp, attr, None)
        if isinstance(v, str):
            return v
    as_d = _as_dict(resp)
    if isinstance(as_d, dict):
        v = as_d.get("result") or as_d.get("value")
        if isinstance(v, str):
            return v
    if isinstance(resp, str):
        return resp
    raise TypeError(f"cannot extract signature from: {type(resp)}")


def get_balance_lamports(
    client: Client,
    pubkey: Pubkey,
    *,
    commitment: Commitment = DEFAULT_COMMITMENT,
) -> int:
    try:
        resp = client.get_balance(pubkey, commitment=commitment)
    except TypeError:
        resp = client.get_balance(pubkey)

    v = getattr(resp, "value", None)
    if isinstance(v, int):
        return v
    as_d = _as_dict(resp) or {}
    return int(((as_d.get("result") or {}).get("value")) or 0)


def wait_for_confirmation(
    client: Client,
    sig: str | Signature,
    *,
    desired: Commitment = DEFAULT_COMMITMENT,
    timeout_sec: float = DEFAULT_TIMEOUT,
    poll_sec: float = DEFAULT_POLL,
) -> dict:
    levels = {"processed": 0, "confirmed": 1, "finalized": 2}
    want = levels[desired]
    t0 = time.time()

    sig_obj = Signature.from_string(sig) if isinstance(sig, str) else sig

    while True:
        try:
            resp = client.get_signature_statuses(
                [sig_obj], search_transaction_history=True
            )
            statuses = getattr(resp, "value", None)
            if statuses is not None:
                st = statuses[0] if statuses else None
                if st is not None:
                    err = getattr(st, "err", None)
                    if err:
                        raise RuntimeError(f"transaction error: {err}")
                    conf_status = getattr(st, "confirmation_status", None)
                    confirmations = getattr(st, "confirmations", None)
                    if conf_status is not None:
                        cs = str(conf_status)
                        if levels.get(cs, -1) >= want:
                            return {
                                "confirmationStatus": cs,
                                "confirmations": confirmations,
                            }
                    elif (
                        isinstance(confirmations, int)
                        and confirmations > 0
                        and want <= 1
                    ):
                        return {
                            "confirmationStatus": "confirmed",
                            "confirmations": confirmations,
                        }
        except Exception:
            pass

        try:
            tx = client.get_transaction(sig_obj, max_supported_transaction_version=0)
            if getattr(tx, "value", None) is not None:
                return {"confirmationStatus": "confirmed", "confirmations": None}
            as_d = _as_dict(tx)
            if isinstance(as_d, dict) and (as_d.get("result") or as_d.get("value")):
                return {"confirmationStatus": "confirmed", "confirmations": None}
        except Exception:
            pass

        if time.time() - t0 > timeout_sec:
            raise TimeoutError(f"confirmation timeout for {sig_obj}")

        time.sleep(poll_sec)


def estimate_fee_for_message(client: Client, msg) -> int:
    try:
        resp = client.get_fee_for_message(msg)
    except TypeError:
        resp = client.get_fee_for_message(message=msg)

    v = getattr(resp, "value", None)
    if isinstance(v, int):
        return v

    as_d = _as_dict(resp) or {}
    val = (as_d.get("result") or {}).get("value")
    if isinstance(val, int):
        return val

    try:
        fees_resp = client.get_fees()
        fd = _as_dict(fees_resp) or {}
        fee_calc = ((fd.get("result") or {}).get("value") or {}).get(
            "feeCalculator"
        ) or {}
        lps = fee_calc.get("lamportsPerSignature")
        if isinstance(lps, int):
            try:
                sigs = getattr(msg, "header", None)
                sigs = (
                    getattr(sigs, "num_required_signatures", 1)
                    if sigs is not None
                    else 1
                )
            except Exception:
                sigs = 1
            return int(lps) * int(sigs)
    except Exception:
        pass

    return 0


def tx_opts(
    skip_preflight: bool = DEFAULT_SKIP_PREFLIGHT,
    commitment: Commitment = DEFAULT_COMMITMENT,
    max_retries: Optional[int] = DEFAULT_MAX_RETRIES,
) -> TxOpts:
    return TxOpts(
        skip_preflight=skip_preflight,
        preflight_commitment=commitment,
        max_retries=max_retries,
    )
