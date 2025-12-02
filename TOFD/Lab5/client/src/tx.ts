import { Connection, Transaction } from "@solana/web3.js";
export const RPC_URL = import.meta.env.VITE_RPC_URL || "https://api.devnet.solana.com";
export function base64ToU8a(b64: string): Uint8Array {
  const bin = atob(b64.trim());
  const out = new Uint8Array(bin.length);
  for (let i = 0; i < bin.length; i++) out[i] = bin.charCodeAt(i);
  return out;
}
export function txFromBase64(b64: string): Transaction {
  return Transaction.from(base64ToU8a(b64));
}
export async function signAndSendRaw(
  connection: Connection,
  wallet: { signTransaction: (t: Transaction) => Promise<Transaction> },
  tx: Transaction,
) {
  const signed = await wallet.signTransaction(tx);
  const sig = await connection.sendRawTransaction(signed.serialize(), { skipPreflight: false });
  await connection.confirmTransaction(sig, "confirmed");
  return sig;
}
