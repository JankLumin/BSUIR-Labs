import * as anchor from '@coral-xyz/anchor';
import {
  Connection,
  Keypair,
  PublicKey,
  SYSVAR_RENT_PUBKEY,
  SystemProgram,
  Transaction,
  SYSVAR_INSTRUCTIONS_PUBKEY
} from '@solana/web3.js';
import {
  ASSOCIATED_TOKEN_PROGRAM_ID,
  ataAddress,
  bankStatePda,
  bankWalletPda,
  cardMetaPda,
  metadataPda,
  masterEditionPda,
  TOKEN_PROGRAM_ID,
  TOKEN_METADATA_PROGRAM_ID,
} from '../utils/pda';
import { Metaplex } from '@metaplex-foundation/js';

async function retry<T>(fn: () => Promise<T>, retries: number, delay: number): Promise<T> {
  for (let i = 0; i < retries; i++) {
    try {
      return await fn();
    } catch (err) {
      if (i === retries - 1) throw err;
      await new Promise(r => setTimeout(r, delay));
    }
  }
  throw new Error('retry failed');
}

export class MintService {
  constructor(
    private readonly connection: Connection,
    private readonly program: any,
  ) {}

  private async finalizeTx(tx: Transaction, feePayer: PublicKey) {
    tx.feePayer = feePayer;
    const { blockhash } = await this.connection.getLatestBlockhash('confirmed');
    tx.recentBlockhash = blockhash;
    return tx;
  }

  async buildMintTx(params: {
    userPubkey: string;
    cardType: number;
    name: string;
    symbol: string;
    uri: string;
  }) {
    const user = new PublicKey(params.userPubkey);
    const mint = Keypair.generate();
    const pid = this.program.programId as PublicKey;

    const tokenAccount = ataAddress(mint.publicKey, user);
    const cardMeta = cardMetaPda(pid, mint.publicKey);
    const metadata = metadataPda(mint.publicKey);
    const masterEdition = masterEditionPda(mint.publicKey);
    const bankState = bankStatePda(pid);
    const bankWallet = bankWalletPda(pid);

    const legacyTx: Transaction = await this.program.methods
      .mintCard(params.cardType, params.name, params.symbol, params.uri)
      .accounts({
        user,
        mint: mint.publicKey,
        tokenAccount,
        metadata,
        masterEdition,
        cardMeta,
        bankWallet,
        bankState,
        tokenProgram: TOKEN_PROGRAM_ID,
        associatedTokenProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
        systemProgram: SystemProgram.programId,
        rent: SYSVAR_RENT_PUBKEY,
        tokenMetadataProgram: TOKEN_METADATA_PROGRAM_ID,
        sysvarInstructions: SYSVAR_INSTRUCTIONS_PUBKEY
      })
      .transaction();

    const tx = await this.finalizeTx(legacyTx, user);
    tx.partialSign(mint);

    return {
      tx: tx.serialize({ requireAllSignatures: false }).toString('base64'),
      mint: mint.publicKey.toBase58(),
      tokenAccount: tokenAccount.toBase58(),
      metadata: metadata.toBase58(),
      masterEdition: masterEdition.toBase58(),
      cardMeta: cardMeta.toBase58(),
      bankState: bankState.toBase58(),
      bankWallet: bankWallet.toBase58(),
      note: 'Подпиши и отправь транзакцию кошельком пользователя.',
    };
  }

  async buildSellTx(params: { userPubkey: string; mint: string }) {
    const user = new PublicKey(params.userPubkey);
    const mint = new PublicKey(params.mint);

    const pid = this.program.programId as PublicKey;
    const bankState = bankStatePda(pid);
    const bankWallet = bankWalletPda(pid);
    const tokenAccount = ataAddress(mint, user);
    const cardMeta = cardMetaPda(pid, mint);

    const legacyTx: Transaction = await this.program.methods
      .sellCard()
      .accounts({
        user,
        bankWallet,
        bankState,
        cardMeta,
        mint,
        tokenAccount,
        tokenProgram: TOKEN_PROGRAM_ID,
        systemProgram: SystemProgram.programId,
      })
      .transaction();

    const tx = await this.finalizeTx(legacyTx, user);

    return {
      tx: tx.serialize({ requireAllSignatures: false }).toString('base64'),
      bankState: bankState.toBase58(),
      bankWallet: bankWallet.toBase58(),
      tokenAccount: tokenAccount.toBase58(),
      cardMeta: cardMeta.toBase58(),
      note: 'Подпиши и отправь транзакцию кошельком владельца NFT. Банк переведёт SOL и сожжёт NFT.',
    };
  }



  
    async getInventory(userPubkey: string) {
      const user = new PublicKey(userPubkey);
      const pid = this.program.programId as PublicKey;

      const allCardMetaAccounts = await this.program.account.cardMeta.all();

      const ownedCards = await Promise.all(
        allCardMetaAccounts.map(async (acc) => {
          const mint = acc.account.mintPubkey;
          const tokenAccount = ataAddress(mint, user);

          let hasBalance = false;
          try {
            const info = await this.connection.getTokenAccountBalance(tokenAccount);
            hasBalance = info.value.amount === '1';
          } catch (e) {
            hasBalance = false;
          }

          return hasBalance ? acc : null;
        })
      );

      const validCards = ownedCards.filter(Boolean) as typeof allCardMetaAccounts;

      ;

      const inventory = await Promise.all(
        validCards.map(async (acc) => {
          const mint = acc.account.mintPubkey;
          const cardType = acc.account.cardType;
          const mintTime = acc.account.mintTime.toNumber();

          let name = ['Rock', 'Paper', 'Scissors'][cardType] || 'Card';
          let symbol = 'DNCG';
          let imageUrl = '';

          try {
            const metadataAccount = metadataPda(mint);
            const info = await this.connection.getAccountInfo(metadataAccount);
            if (info && info.data.length > 100) {
              const d = info.data;

              let off = 1 + 32 + 32; // type + mint_auth + update_auth
              let len = d.readUInt32LE(off); off += 4;
              name = d.slice(off, off + len).toString('utf8').replace(/\0/g, '').trim();
              off += len;
              len = d.readUInt32LE(off); off += 4;
              symbol = d.slice(off, off + len).toString('utf8').replace(/\0/g, '').trim();
              off += len;
              len = d.readUInt32LE(off); off += 4;
              const uri = d.slice(off, off + len).toString('utf8').replace(/\0/g, '').trim();

              if (uri) {
                try {
                  const res = await fetch(uri, { signal: AbortSignal.timeout(5000) });
                  if (res.ok) {
                    const json = await res.json();
                    imageUrl = json.image || '';
                  }
                } catch {}
              }
            }
          } catch (e) {
            console.warn('Metadata parse error:', mint.toBase58());
          }

          return {
            mint: mint.toBase58(),
            name: name || ['Rock', 'Paper', 'Scissors'][cardType],
            symbol,
            uri: imageUrl,
            cardType,
            mintTime: new Date(mintTime * 1000).toLocaleString('ru-RU'),
          };
        })
      );

      return { inventory };
    }
}
