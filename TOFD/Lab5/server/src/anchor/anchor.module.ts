import 'dotenv/config';
import { Module, Global } from '@nestjs/common';
import * as anchor from '@coral-xyz/anchor';
import { Connection, Keypair, PublicKey } from '@solana/web3.js';
import * as fs from 'fs';
import * as path from 'path';

function loadAdminKeypair(): Keypair {
  const p = process.env.ADMIN_KEYPAIR_PATH;
  const raw = process.env.ADMIN_SECRET_KEY;
  if (p && fs.existsSync(p)) {
    const bytes = JSON.parse(fs.readFileSync(p, 'utf8'));
    return Keypair.fromSecretKey(Uint8Array.from(bytes));
  }
  if (raw) {
    const bytes = JSON.parse(raw);
    return Keypair.fromSecretKey(Uint8Array.from(bytes));
  }
  throw new Error('ADMIN_SECRET_KEY или ADMIN_KEYPAIR_PATH не заданы');
}

function loadIdl(): any {
  const idlPath = path.join(
    process.cwd(),
    'src',
    'anchor',
    'idl',
    'dncg_program.json',
  );
  if (!fs.existsSync(idlPath)) {
    throw new Error(
      `IDL not found at ${idlPath}. Скопируй target/idl/dncg_program.json сюда.`,
    );
  }
  const idl = JSON.parse(fs.readFileSync(idlPath, 'utf8'));
  if (!idl.address) {
    idl.address = process.env.PROGRAM_ID;
  }
  return idl;
}

@Global()
@Module({
  providers: [
    {
      provide: 'CONNECTION',
      useFactory: () =>
        new Connection(process.env.RPC_URL!, { commitment: 'confirmed' }),
    },
    {
      provide: 'ADMIN_KEYPAIR',
      useFactory: () => loadAdminKeypair(),
    },
    {
      provide: 'ADMIN_PROVIDER',
      useFactory: (conn: Connection, kp: Keypair) => {
        const wallet = new anchor.Wallet(kp);
        const provider = new anchor.AnchorProvider(conn, wallet, {
          preflightCommitment: 'confirmed',
          commitment: 'confirmed',
        });
        anchor.setProvider(provider);
        return provider;
      },
      inject: ['CONNECTION', 'ADMIN_KEYPAIR'],
    },
    {
      provide: 'PROGRAM',
      useFactory: (provider: anchor.AnchorProvider) => {
        const idl = loadIdl();
        const program = new anchor.Program(idl as anchor.Idl, provider);
        return program;
      },
      inject: ['ADMIN_PROVIDER'],
    },
  ],
  exports: ['CONNECTION', 'ADMIN_PROVIDER', 'PROGRAM'],
})
export class AnchorModule {}
