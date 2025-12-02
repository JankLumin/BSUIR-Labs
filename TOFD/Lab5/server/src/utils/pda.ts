import { PublicKey } from '@solana/web3.js';

export const SYSTEM_PROGRAM_ID = new PublicKey(
  '11111111111111111111111111111111',
);
export const TOKEN_PROGRAM_ID = new PublicKey(
  'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA',
);
export const ASSOCIATED_TOKEN_PROGRAM_ID = new PublicKey(
  'ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL',
);
export const TOKEN_METADATA_PROGRAM_ID = new PublicKey(
  'metaqbxxUerdq28cj1RbAWkYQm3ybzjb6a8bt518x1s',
);

export function masterEditionPda(mint: PublicKey) {
  return PublicKey.findProgramAddressSync(
    [
      Buffer.from('metadata'),
      TOKEN_METADATA_PROGRAM_ID.toBuffer(),
      mint.toBuffer(),
      Buffer.from('edition'),
    ],
    TOKEN_METADATA_PROGRAM_ID
  )[0];
}


export function bankStatePda(programId: PublicKey) {
  return PublicKey.findProgramAddressSync(
    [Buffer.from('bank_state')],
    programId,
  )[0];
}
export function bankWalletPda(programId: PublicKey) {
  return PublicKey.findProgramAddressSync([Buffer.from('bank')], programId)[0];
}
export function cardMetaPda(programId: PublicKey, mint: PublicKey) {
  return PublicKey.findProgramAddressSync(
    [Buffer.from('card'), mint.toBuffer()],
    programId,
  )[0];
}
export function matchPda(programId: PublicKey, matchId: bigint) {
  const le = Buffer.alloc(8);
  le.writeBigUInt64LE(matchId);
  return PublicKey.findProgramAddressSync(
    [Buffer.from('match'), le],
    programId,
  )[0];
}
export function ataAddress(mint: PublicKey, owner: PublicKey) {
  return PublicKey.findProgramAddressSync(
    [owner.toBuffer(), TOKEN_PROGRAM_ID.toBuffer(), mint.toBuffer()],
    ASSOCIATED_TOKEN_PROGRAM_ID,
  )[0];
}
export function metadataPda(mint: PublicKey) {
  return PublicKey.findProgramAddressSync(
    [
      Buffer.from('metadata'),
      TOKEN_METADATA_PROGRAM_ID.toBuffer(),
      mint.toBuffer(),
    ],
    TOKEN_METADATA_PROGRAM_ID,
  )[0];
}
