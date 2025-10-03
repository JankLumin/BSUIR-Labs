import * as anchor from "@coral-xyz/anchor";
import { BN, Program } from "@coral-xyz/anchor";
import { PublicKey, SystemProgram, SYSVAR_RENT_PUBKEY, Transaction } from "@solana/web3.js";
import {
  ASSOCIATED_TOKEN_PROGRAM_ID,
  TOKEN_PROGRAM_ID,
  NATIVE_MINT,
  getAssociatedTokenAddressSync,
  createAssociatedTokenAccountIdempotentInstruction,
  createSyncNativeInstruction,
  getAccount,
  getMint,
} from "@solana/spl-token";
import idl from "../target/idl/dex_app.json";
import "dotenv/config";


function uiToAmount(value: number, decimals: number): bigint {
  const s = String(value);
  const [i, fRaw = ""] = s.split(".");
  const f = (fRaw + "0".repeat(decimals)).slice(0, decimals);
  return BigInt(i + f);
}
function fmt(amount: bigint, decimals: number): string {
  const s = amount.toString().padStart(decimals + 1, "0");
  const head = s.slice(0, -decimals) || "0";
  const tail = s.slice(-decimals).replace(/0+$/, "");
  return tail ? `${head}.${tail}` : head;
}
async function getBal(conn: anchor.web3.Connection, ata: PublicKey): Promise<bigint> {
  try {
    const acc = await getAccount(conn, ata);
    return BigInt(acc.amount.toString());
  } catch {
    return 0n;
  }
}
async function ensureWsol(provider: anchor.AnchorProvider, owner: PublicKey, lamports: number) {
  const ata = getAssociatedTokenAddressSync(NATIVE_MINT, owner);
  const ixs = [
    createAssociatedTokenAccountIdempotentInstruction(owner, ata, owner, NATIVE_MINT),
    SystemProgram.transfer({ fromPubkey: owner, toPubkey: ata, lamports }),
    createSyncNativeInstruction(ata),
  ];
  await provider.sendAndConfirm(new Transaction().add(...ixs));
  return ata;
}
function logSection(title: string) {
  console.log("\n" + "—".repeat(70));
  console.log(title);
  console.log("—".repeat(70));
}

(async () => {
  const MINT = process.env.MINT;
  if (!MINT) throw new Error("Set MINT=<your local token mint pubkey>");

  const ACTION = (process.env.ACTION || "init+buy+sell").toLowerCase();

  const INIT_YOUR_UI = parseFloat(process.env.INIT_YOUR_UI || "1");
  const INIT_WSOL_UI = parseFloat(process.env.INIT_WSOL_UI || "0.5");
  const BUY_WSOL_UI = parseFloat(process.env.BUY_WSOL_UI || "0.1");
  const SELL_YOUR_UI = parseFloat(process.env.SELL_YOUR_UI || "0.05");

  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);

  const ENV_PID = process.env.PROGRAM_ID;
  if (ENV_PID) {
    (idl as any).metadata = (idl as any).metadata || {};
    (idl as any).metadata.address = ENV_PID;
    (idl as any).address = ENV_PID;
  }
  const program = new Program(idl as anchor.Idl, provider) as Program<any>;

  const yourMint = new PublicKey(MINT);
  const wsolMint = NATIVE_MINT;
  const yourMintAcc = await getMint(provider.connection, yourMint);
  const wsolMintAcc = await getMint(provider.connection, wsolMint);
  const dYour = yourMintAcc.decimals;
  const dWsol = wsolMintAcc.decimals;

  const user = provider.wallet.publicKey;
  const userYourAta = getAssociatedTokenAddressSync(yourMint, user);
  const userWsolAta = getAssociatedTokenAddressSync(wsolMint, user);
  await provider.sendAndConfirm(
    new Transaction().add(
      createAssociatedTokenAccountIdempotentInstruction(user, userYourAta, user, yourMint),
      createAssociatedTokenAccountIdempotentInstruction(user, userWsolAta, user, wsolMint),
    ),
  );

  await ensureWsol(provider, user, 1_000_000_000);

  const POOL_FROM_ENV = process.env.POOL;
  const poolKp = POOL_FROM_ENV ? null : anchor.web3.Keypair.generate();
  const poolPk = POOL_FROM_ENV
    ? new PublicKey(POOL_FROM_ENV)
    : (poolKp as anchor.web3.Keypair).publicKey;
  const [poolAuthority] = PublicKey.findProgramAddressSync(
    [Buffer.from("pool"), poolPk.toBuffer()],
    program.programId,
  );
  const poolYourAta = getAssociatedTokenAddressSync(yourMint, poolAuthority, true);
  const poolWsolAta = getAssociatedTokenAddressSync(wsolMint, poolAuthority, true);

  const uYour0 = await getBal(provider.connection, userYourAta);
  const uWsol0 = await getBal(provider.connection, userWsolAta);
  const pYour0 = await getBal(provider.connection, poolYourAta);
  const pWsol0 = await getBal(provider.connection, poolWsolAta);

  logSection("== BEFORE ==");
  console.log("Program ID   :", program.programId.toBase58());
  console.log("Pool         :", poolPk.toBase58());
  console.log("PoolAuth (PDA):", poolAuthority.toBase58());
  console.log("Pool ATA YOUR:", poolYourAta.toBase58());
  console.log("Pool ATA WSOL:", poolWsolAta.toBase58());
  console.log("User YOUR    :", `${uYour0}  (${fmt(uYour0, dYour)} YOUR)`);
  console.log("User WSOL    :", `${uWsol0}  (${fmt(uWsol0, dWsol)} WSOL)`);
  console.log("Pool YOUR    :", `${pYour0}  (${fmt(pYour0, dYour)} YOUR)`);
  console.log("Pool WSOL    :", `${pWsol0}  (${fmt(pWsol0, dWsol)} WSOL)`);

  const rateNum = 1n;
  const rateDen = 2n;

  if (ACTION.includes("init")) {
    if (!poolKp) throw new Error("Provide ACTION=buy/sell only if POOL is set");
    const initYour = uiToAmount(INIT_YOUR_UI, dYour);
    const initWsol = uiToAmount(INIT_WSOL_UI, dWsol);

    logSection("→ initialize (add liquidity)");
    console.log(
      `init YOUR = ${initYour} (${INIT_YOUR_UI} YOUR), init WSOL = ${initWsol} (${INIT_WSOL_UI} WSOL)`,
    );

    await program.methods
      .initialize(new BN(initYour.toString()), new BN(initWsol.toString()))
      .accounts({
        pool: poolPk,
        poolAuthority,
        yourMint,
        wsolMint,
        poolYourAta,
        poolWsolAta,
        userYourAta,
        userWsolAta,
        payer: user,
        systemProgram: SystemProgram.programId,
        tokenProgram: TOKEN_PROGRAM_ID,
        associatedTokenProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
        rent: SYSVAR_RENT_PUBKEY,
      })
      .signers([poolKp])
      .rpc();
    console.log("Pool initialized:", poolPk.toBase58());
  }

  if (ACTION.includes("buy")) {
    const amountWsolIn = uiToAmount(BUY_WSOL_UI, dWsol);
    const yourOut =
      (amountWsolIn * 10n ** BigInt(dYour) * rateDen) / (rateNum * 10n ** BigInt(dWsol));

    logSection("→ buy");
    console.log(
      `user pays ${amountWsolIn} WSOL (${BUY_WSOL_UI} WSOL) — expected receive YOUR ≈ ${yourOut} (${fmt(
        yourOut,
        dYour,
      )})`,
    );

    const uuY0 = await getBal(provider.connection, userYourAta);
    const uuW0 = await getBal(provider.connection, userWsolAta);
    const ppY0 = await getBal(provider.connection, poolYourAta);
    const ppW0 = await getBal(provider.connection, poolWsolAta);

    await program.methods
      .buy(new BN(amountWsolIn.toString()))
      .accounts({
        pool: poolPk,
        poolAuthority,
        poolYourAta,
        poolWsolAta,
        userYourAta,
        userWsolAta,
        user,
        tokenProgram: TOKEN_PROGRAM_ID,
      })
      .rpc();

    const uuY1 = await getBal(provider.connection, userYourAta);
    const uuW1 = await getBal(provider.connection, userWsolAta);
    const ppY1 = await getBal(provider.connection, poolYourAta);
    const ppW1 = await getBal(provider.connection, poolWsolAta);

    console.log("User ΔYOUR:", (uuY1 - uuY0).toString(), `(${fmt(uuY1 - uuY0, dYour)})`);
    console.log("User ΔWSOL:", (uuW1 - uuW0).toString(), `(${fmt(uuW1 - uuW0, dWsol)})`);
    console.log("Pool ΔYOUR:", (ppY1 - ppY0).toString(), `(${fmt(ppY1 - ppY0, dYour)})`);
    console.log("Pool ΔWSOL:", (ppW1 - ppW0).toString(), `(${fmt(ppW1 - ppW0, dWsol)})`);
  }

  if (ACTION.includes("sell")) {
    const amountYourIn = uiToAmount(SELL_YOUR_UI, dYour);
    const wsolOut =
      (amountYourIn * 10n ** BigInt(dWsol) * rateNum) / (rateDen * 10n ** BigInt(dYour));

    logSection("→ sell");
    console.log(
      `user pays ${amountYourIn} YOUR (${SELL_YOUR_UI} YOUR) — expected receive WSOL ≈ ${wsolOut} (${fmt(
        wsolOut,
        dWsol,
      )})`,
    );

    const uuY0 = await getBal(provider.connection, userYourAta);
    const uuW0 = await getBal(provider.connection, userWsolAta);
    const ppY0 = await getBal(provider.connection, poolYourAta);
    const ppW0 = await getBal(provider.connection, poolWsolAta);

    await program.methods
      .sell(new BN(amountYourIn.toString()))
      .accounts({
        pool: poolPk,
        poolAuthority,
        poolYourAta,
        poolWsolAta,
        userYourAta,
        userWsolAta,
        user,
        tokenProgram: TOKEN_PROGRAM_ID,
      })
      .rpc();

    const uuY1 = await getBal(provider.connection, userYourAta);
    const uuW1 = await getBal(provider.connection, userWsolAta);
    const ppY1 = await getBal(provider.connection, poolYourAta);
    const ppW1 = await getBal(provider.connection, poolWsolAta);

    console.log("User ΔYOUR:", (uuY1 - uuY0).toString(), `(${fmt(uuY1 - uuY0, dYour)})`);
    console.log("User ΔWSOL:", (uuW1 - uuW0).toString(), `(${fmt(uuW1 - uuW0, dWsol)})`);
    console.log("Pool ΔYOUR:", (ppY1 - ppY0).toString(), `(${fmt(ppY1 - ppY0, dYour)})`);
    console.log("Pool ΔWSOL:", (ppW1 - ppW0).toString(), `(${fmt(ppW1 - ppW0, dWsol)})`);
  }

  const uYour1 = await getBal(provider.connection, userYourAta);
  const uWsol1 = await getBal(provider.connection, userWsolAta);
  const pYour1 = await getBal(provider.connection, poolYourAta);
  const pWsol1 = await getBal(provider.connection, poolWsolAta);

  logSection("== AFTER ==");
  console.log("User YOUR    :", `${uYour1}  (${fmt(uYour1, dYour)} YOUR)`);
  console.log("User WSOL    :", `${uWsol1}  (${fmt(uWsol1, dWsol)} WSOL)`);
  console.log("Pool YOUR    :", `${pYour1}  (${fmt(pYour1, dYour)} YOUR)`);
  console.log("Pool WSOL    :", `${pWsol1}  (${fmt(pWsol1, dWsol)} WSOL)`);
  console.log("Δ User YOUR  :", (uYour1 - uYour0).toString(), `(${fmt(uYour1 - uYour0, dYour)})`);
  console.log("Δ User WSOL  :", (uWsol1 - uWsol0).toString(), `(${fmt(uWsol1 - uWsol0, dWsol)})`);
  console.log("Δ Pool YOUR  :", (pYour1 - pYour0).toString(), `(${fmt(pYour1 - pYour0, dYour)})`);
  console.log("Δ Pool WSOL  :", (pWsol1 - pWsol0).toString(), `(${fmt(pWsol1 - pWsol0, dWsol)})`);
})().catch((e) => {
  console.error(e);
  process.exit(1);
});
