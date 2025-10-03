import "dotenv/config";
import * as fs from "fs";
import * as path from "path";
import * as anchor from "@coral-xyz/anchor";
import { Connection, Keypair, PublicKey, SystemProgram } from "@solana/web3.js";
import idl from "../target/idl/counter_app.json";

function loadKeypair(p: string): Keypair {
  const raw = fs.readFileSync(p, "utf8");
  const secret = Uint8Array.from(JSON.parse(raw));
  return Keypair.fromSecretKey(secret);
}

async function main() {
  const RPC = process.env.ANCHOR_PROVIDER_URL!;
  const WALLET_PATH = process.env.ANCHOR_WALLET!;
  const PROGRAM_ID = new PublicKey(process.env.PROGRAM_ID ?? (idl as any).address);

  if (!RPC || !WALLET_PATH) {
    throw new Error("Set ANCHOR_PROVIDER_URL and ANCHOR_WALLET in .env");
  }

  const connection = new Connection(RPC, "confirmed");
  const walletKp = loadKeypair(path.resolve(WALLET_PATH));
  const wallet = new anchor.Wallet(walletKp);
  const provider = new anchor.AnchorProvider(connection, wallet, {
    commitment: "confirmed",
  });
  anchor.setProvider(provider);

  const program = new anchor.Program(idl as anchor.Idl, provider);

  const counterKp = Keypair.generate();

  console.log("→ initialize");
  const sigInit = await program.methods
    .initialize()
    .accountsStrict({
      counter: counterKp.publicKey,
      authority: wallet.publicKey,
      systemProgram: SystemProgram.programId,
    })
    .signers([counterKp])
    .rpc();
  console.log("  tx:", sigInit);

  console.log("→ increment ×3");
  for (let i = 0; i < 3; i++) {
    const sig = await program.methods
      .increment()
      .accountsStrict({
        counter: counterKp.publicKey,
        authority: wallet.publicKey,
      })
      .rpc();
    console.log(`  inc ${i + 1}:`, sig);
  }

  console.log("→ decrement ×1");
  const sigDec = await program.methods
    .decrement()
    .accountsStrict({
      counter: counterKp.publicKey,
      authority: wallet.publicKey,
    })
    .rpc();
  console.log("  tx:", sigDec);

  const acc = (await (program.account as any).counterAcc.fetch(counterKp.publicKey)) as {
    value: anchor.BN;
    authority: PublicKey;
  };

  console.log("—".repeat(60));
  console.log("Program ID    :", PROGRAM_ID.toBase58());
  console.log("Counter pubkey:", counterKp.publicKey.toBase58());
  console.log("Current value :", acc.value.toString());
  console.log("Authority     :", acc.authority.toBase58());
  console.log("—".repeat(60));
}

main().catch((e) => {
  console.error(e);
  process.exit(1);
});
