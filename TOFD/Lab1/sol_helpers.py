from __future__ import annotations

import argparse
import sys

from common import (
    LAMPORTS_PER_SOL,
    Commitment,
    DEFAULT_COMMITMENT,
    DEFAULT_TIMEOUT,
    DEFAULT_POLL,
    DEFAULT_SKIP_PREFLIGHT,
    DEFAULT_MAX_RETRIES,
    get_client,
    load_keypair,
    resolve_pubkey,
    extract_sig,
    wait_for_confirmation,
    save_keypair,
    get_balance_lamports,
    _as_dict,
    estimate_fee_for_message,
    tx_opts,
)
from solders.keypair import Keypair
from solders.system_program import transfer, TransferParams
from solders.message import Message
from solders.hash import Hash
from solders.transaction import Transaction


def _parse_amount_to_lamports(value: str) -> int:
    v = str(value).strip().lower()
    v = v.replace("_", "").replace(",", "")
    v_no_sp = v.replace(" ", "")

    if v_no_sp.endswith("sol"):
        sol = float(v_no_sp[:-3])
        return int(round(sol * LAMPORTS_PER_SOL))

    if v_no_sp.endswith(("lamports", "lamport", "lam")):
        num = v.split()[0]
        return int(num)

    if any(ch in v for ch in ".e"):
        return int(round(float(v) * LAMPORTS_PER_SOL))

    return int(v) * LAMPORTS_PER_SOL


def _get_recent_blockhash(client, commitment: Commitment = DEFAULT_COMMITMENT) -> Hash:
    try:
        lb = client.get_latest_blockhash(commitment=commitment)
    except TypeError:
        lb = client.get_latest_blockhash()

    val = getattr(lb, "value", None)
    if val is not None:
        bh_obj = getattr(val, "blockhash", None)
        if isinstance(bh_obj, Hash):
            return bh_obj
        if bh_obj is not None:
            try:
                return Hash.from_string(str(bh_obj))
            except Exception:
                pass

    if isinstance(lb, dict):
        val = lb.get("value") or (lb.get("result") or {}).get("value")
        if isinstance(val, dict):
            bh = val.get("blockhash")
            if isinstance(bh, str):
                return Hash.from_string(bh)

    raise RuntimeError(f"Cannot extract blockhash from response: {lb!r}")


def _print_fee_from_tx_meta(client, sig: str) -> None:
    try:
        tx = client.get_transaction(sig, max_supported_transaction_version=0)
        d = _as_dict(tx) or {}
        meta = ((d.get("result") or d.get("value") or {}) or {}).get("meta") or {}
        fee = meta.get("fee")
        if fee is not None:
            print(
                f"[i] Actual fee:      {fee} lamports ({fee / LAMPORTS_PER_SOL:.9f} SOL)"
            )
        pre = meta.get("preBalances") or []
        post = meta.get("postBalances") or []
        if pre and post and len(pre) == len(post):
            print("    Balances delta (lamports):")
            for i, (pb, qb) in enumerate(zip(pre, post)):
                delta = qb - pb
                print(f"      [{i}] {pb} -> {qb} (Δ {delta})")
    except Exception:
        pass


def cmd_create(a: argparse.Namespace):
    kp = Keypair()
    save_keypair(kp, a.out)
    print(f"[OK] Keypair saved to: {a.out}")


def cmd_balance(a: argparse.Namespace):
    c = get_client(a.url)
    pk = resolve_pubkey(a.pubkey_or_file)
    lam = get_balance_lamports(c, pk, commitment=DEFAULT_COMMITMENT)
    print(f"Balance: {lam} lamports ({lam / LAMPORTS_PER_SOL:.9f} SOL)")


def cmd_airdrop(a: argparse.Namespace):
    c = get_client(a.url)
    to_pk = resolve_pubkey(a.to_pubkey_or_file)
    lamports = _parse_amount_to_lamports(a.amount)

    before = get_balance_lamports(c, to_pk, commitment=DEFAULT_COMMITMENT)
    print(
        f"[i] Balance before: {before} lamports ({before / LAMPORTS_PER_SOL:.9f} SOL)"
    )

    resp = c.request_airdrop(to_pk, lamports)
    sig = extract_sig(resp)
    print("[OK] Airdrop signature:", sig)

    st = wait_for_confirmation(
        c,
        sig,
        desired=DEFAULT_COMMITMENT,
        timeout_sec=DEFAULT_TIMEOUT,
        poll_sec=DEFAULT_POLL,
    )
    after = get_balance_lamports(c, to_pk, commitment=DEFAULT_COMMITMENT)
    print(f"[i] Balance after:  {after} lamports ({after / LAMPORTS_PER_SOL:.9f} SOL)")
    print("[OK] Status:", st.get("confirmationStatus"))


def cmd_transfer(a: argparse.Namespace):
    c = get_client(a.url)
    sender = load_keypair(a.from_path)
    to_pk = resolve_pubkey(a.to_pubkey_or_file)
    amount = _parse_amount_to_lamports(a.amount)

    s_before = get_balance_lamports(c, sender.pubkey(), commitment=DEFAULT_COMMITMENT)
    r_before = get_balance_lamports(c, to_pk, commitment=DEFAULT_COMMITMENT)
    print(
        f"[i] Sender before:    {s_before} lamports ({s_before / LAMPORTS_PER_SOL:.9f} SOL)"
    )
    print(
        f"[i] Recipient before: {r_before} lamports ({r_before / LAMPORTS_PER_SOL:.9f} SOL)"
    )

    ix = transfer(
        TransferParams(from_pubkey=sender.pubkey(), to_pubkey=to_pk, lamports=amount)
    )
    recent = _get_recent_blockhash(c, DEFAULT_COMMITMENT)
    msg = Message.new_with_blockhash([ix], sender.pubkey(), recent)

    fee_est = estimate_fee_for_message(c, msg)
    need = amount + fee_est
    if s_before < need:
        raise SystemExit(
            f"Insufficient funds: need {need} lamports (amount={amount} + fee≈{fee_est}), have {s_before}."
        )

    tx = Transaction(from_keypairs=[sender], message=msg, recent_blockhash=recent)
    opts = tx_opts(DEFAULT_SKIP_PREFLIGHT, DEFAULT_COMMITMENT, DEFAULT_MAX_RETRIES)
    resp = c.send_raw_transaction(bytes(tx), opts=opts)
    sig = extract_sig(resp)
    print("[OK] Transfer signature:", sig)

    st = wait_for_confirmation(
        c,
        sig,
        desired=DEFAULT_COMMITMENT,
        timeout_sec=DEFAULT_TIMEOUT,
        poll_sec=DEFAULT_POLL,
    )
    _print_fee_from_tx_meta(c, sig)
    s_after = get_balance_lamports(c, sender.pubkey(), commitment=DEFAULT_COMMITMENT)
    r_after = get_balance_lamports(c, to_pk, commitment=DEFAULT_COMMITMENT)
    print(
        f"[i] Sender after:     {s_after} lamports ({s_after / LAMPORTS_PER_SOL:.9f} SOL)"
    )
    print(
        f"[i] Recipient after:  {r_after} lamports ({r_after / LAMPORTS_PER_SOL:.9f} SOL)"
    )
    print("[OK] Status:", st.get("confirmationStatus"))


def cmd_sweep(a: argparse.Namespace):
    c = get_client(a.url)
    sender = load_keypair(a.from_path)
    to_pk = resolve_pubkey(a.to_pubkey_or_file)
    fee_buf = 5000

    bal = get_balance_lamports(c, sender.pubkey(), commitment=DEFAULT_COMMITMENT)
    if bal <= 0:
        raise SystemExit("nothing to send (zero balance)")

    tmp_amt = max(0, bal - fee_buf)
    if tmp_amt == 0:
        raise SystemExit(f"nothing to send (balance {bal} <= fee buffer {fee_buf})")

    ix_tmp = transfer(
        TransferParams(from_pubkey=sender.pubkey(), to_pubkey=to_pk, lamports=tmp_amt)
    )
    recent = _get_recent_blockhash(c, DEFAULT_COMMITMENT)
    msg_tmp = Message.new_with_blockhash([ix_tmp], sender.pubkey(), recent)
    fee_est = estimate_fee_for_message(c, msg_tmp)

    reserve = max(fee_buf, fee_est)
    amt = bal - reserve
    if amt <= 0:
        raise SystemExit(
            f"nothing to send after reserving fee: balance {bal}, reserve {reserve}"
        )

    s_before = bal
    r_before = get_balance_lamports(c, to_pk, commitment=DEFAULT_COMMITMENT)
    print(
        f"[i] Sender before:    {s_before} lamports ({s_before / LAMPORTS_PER_SOL:.9f} SOL)"
    )
    print(
        f"[i] Recipient before: {r_before} lamports ({r_before / LAMPORTS_PER_SOL:.9f} SOL)"
    )
    print(f"[i] Planned amount:   {amt} lamports (reserve {reserve})")

    ix = transfer(
        TransferParams(from_pubkey=sender.pubkey(), to_pubkey=to_pk, lamports=amt)
    )
    recent = _get_recent_blockhash(c, DEFAULT_COMMITMENT)
    msg = Message.new_with_blockhash([ix], sender.pubkey(), recent)

    fee_est2 = estimate_fee_for_message(c, msg)
    if fee_est2 > reserve:
        new_reserve = fee_est2
        new_amt = bal - new_reserve
        if new_amt <= 0:
            raise SystemExit(
                f"nothing to send after final fee estimate: balance {bal}, fee {fee_est2}"
            )
        amt = new_amt
        print(
            f"[i] Fee changed on recheck: {fee_est2}. New amount: {amt} (reserve {new_reserve})"
        )
        ix = transfer(
            TransferParams(from_pubkey=sender.pubkey(), to_pubkey=to_pk, lamports=amt)
        )
        recent = _get_recent_blockhash(c, DEFAULT_COMMITMENT)
        msg = Message.new_with_blockhash([ix], sender.pubkey(), recent)

    tx = Transaction(from_keypairs=[sender], message=msg, recent_blockhash=recent)
    opts = tx_opts(DEFAULT_SKIP_PREFLIGHT, DEFAULT_COMMITMENT, DEFAULT_MAX_RETRIES)
    resp = c.send_raw_transaction(bytes(tx), opts=opts)
    sig = extract_sig(resp)
    print(f"[OK] Swept {amt} lamports. Signature:", sig)

    st = wait_for_confirmation(
        c,
        sig,
        desired=DEFAULT_COMMITMENT,
        timeout_sec=DEFAULT_TIMEOUT,
        poll_sec=DEFAULT_POLL,
    )
    _print_fee_from_tx_meta(c, sig)
    s_after = get_balance_lamports(c, sender.pubkey(), commitment=DEFAULT_COMMITMENT)
    r_after = get_balance_lamports(c, to_pk, commitment=DEFAULT_COMMITMENT)
    print(
        f"[i] Sender after:     {s_after} lamports ({s_after / LAMPORTS_PER_SOL:.9f} SOL)"
    )
    print(
        f"[i] Recipient after:  {r_after} lamports ({r_after / LAMPORTS_PER_SOL:.9f} SOL)"
    )
    print("[OK] Status:", st.get("confirmationStatus"))


class CustomArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_usage(sys.stderr)
        self.exit(2, f"error: {message}\n")


def build_parser() -> argparse.ArgumentParser:
    fmt = lambda prog: argparse.HelpFormatter(prog, max_help_position=28, width=120)
    p = CustomArgumentParser(
        prog="sol_helper",
        description="Solana helper",
        add_help=False,
        formatter_class=fmt,
    )
    p.add_argument(
        "--url",
        default="http://127.0.0.1:8899",
        help="RPC URL (devnet: https://api.devnet.solana.com)",
    )

    sub = p.add_subparsers(dest="cmd", metavar="command", required=True)

    s = sub.add_parser(
        "create", help="create keypair", add_help=False, formatter_class=fmt
    )
    s.add_argument("out", help="path to save keypair (JSON)")
    s.set_defaults(func=cmd_create)

    s = sub.add_parser(
        "balance", help="show balance", add_help=False, formatter_class=fmt
    )
    s.add_argument("pubkey_or_file", help="pubkey OR keypair file")
    s.set_defaults(func=cmd_balance)

    s = sub.add_parser(
        "airdrop",
        help="airdrop amount (SOL/lamports)",
        add_help=False,
        formatter_class=fmt,
    )
    s.add_argument("to_pubkey_or_file", help="recipient pubkey OR keypair file")
    s.add_argument("amount", help="amount: '1', '0.01', '0.01SOL', '1500000lam'")
    s.set_defaults(func=cmd_airdrop)

    s = sub.add_parser(
        "transfer",
        help="send amount (net to recipient)",
        add_help=False,
        formatter_class=fmt,
    )
    s.add_argument("from_path", help="sender keypair json (FILE!)")
    s.add_argument("to_pubkey_or_file", help="recipient pubkey OR keypair file")
    s.add_argument("amount", help="amount: '1', '0.01', '0.01SOL', '1500000lam'")
    s.set_defaults(func=cmd_transfer)

    s = sub.add_parser(
        "sweep",
        help="send all (minus 5000 lamports fee buffer)",
        add_help=False,
        formatter_class=fmt,
    )
    s.add_argument("from_path", help="sender keypair json (FILE!)")
    s.add_argument("to_pubkey_or_file", help="recipient pubkey OR keypair file")
    s.set_defaults(func=cmd_sweep)

    return p


def main():
    p = build_parser()
    if len(sys.argv) == 1:
        p.print_help(sys.stderr)
        sys.exit(0)

    try:
        a = p.parse_args()
        if not hasattr(a, "func"):
            p.print_usage(sys.stderr)
            sys.exit(2)
        a.func(a)
    except KeyboardInterrupt:
        sys.exit(130)


if __name__ == "__main__":
    main()
