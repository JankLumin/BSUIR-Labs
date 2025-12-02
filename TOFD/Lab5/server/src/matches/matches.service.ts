import * as anchor from '@coral-xyz/anchor';
import {
  Connection,
  PublicKey,
  SystemProgram,
  SYSVAR_RENT_PUBKEY,
  Transaction,
  TransactionInstruction,
} from '@solana/web3.js';
import {
  ASSOCIATED_TOKEN_PROGRAM_ID,
  ataAddress,
  cardMetaPda,
  matchPda,
  TOKEN_PROGRAM_ID,
} from '../utils/pda';

const STATUS_OPEN = 0;
const STATUS_ACTIVE = 1;
const STATUS_FINISHED = 2;

export class MatchesService {

  private cache: any[] = [];
  private lastFetch = 0;
  private readonly CACHE_TTL = 15000;


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

  async buildCreateTx(params: {
    userPubkey: string;
    matchId: string;
    creatorMint: string;
  }) {
    const creator = new PublicKey(params.userPubkey);
    const creatorMint = new PublicKey(params.creatorMint);
    const pid = this.program.programId as PublicKey;

    const matchIdBig = BigInt(params.matchId);
    const matchAccount = matchPda(pid, matchIdBig);
    const creatorTokenAccount = ataAddress(creatorMint, creator);
    const escrowCreator = ataAddress(creatorMint, matchAccount);
    const cardMeta = cardMetaPda(pid, creatorMint);

    const legacyTx: Transaction = await this.program.methods
      .createMatch(new anchor.BN(params.matchId))
      .accounts({
        creator,
        matchAccount,
        creatorMint,
        creatorTokenAccount,
        cardMeta,
        escrowCreator,
        tokenProgram: TOKEN_PROGRAM_ID,
        associatedTokenProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
        systemProgram: SystemProgram.programId,
      })
      .transaction();

    const tx = await this.finalizeTx(legacyTx, creator);

    return {
      tx: tx.serialize({ requireAllSignatures: false }).toString('base64'),
      matchAccount: matchAccount.toBase58(),
      escrowCreator: escrowCreator.toBase58(),
      creatorTokenAccount: creatorTokenAccount.toBase58(),
      note: 'Подпиши и отправь транзакцию кошельком создателя матча.',
    };
  }

  private async maybeCreateAtaIx(
    owner: PublicKey,
    mint: PublicKey,
    ata: PublicKey,
    payer: PublicKey,
  ) {
    const info = await this.connection.getAccountInfo(ata);
    if (info) return null;
    const keys = [
      { pubkey: payer, isSigner: true, isWritable: true },
      { pubkey: ata, isSigner: false, isWritable: true },
      { pubkey: owner, isSigner: false, isWritable: false },
      { pubkey: mint, isSigner: false, isWritable: false },
      { pubkey: TOKEN_PROGRAM_ID, isSigner: false, isWritable: false },
      { pubkey: SystemProgram.programId, isSigner: false, isWritable: false },
      { pubkey: SYSVAR_RENT_PUBKEY, isSigner: false, isWritable: false },
    ];
    return new TransactionInstruction({
      programId: ASSOCIATED_TOKEN_PROGRAM_ID,
      keys,
      data: Buffer.alloc(0),
    });
  }

  async buildJoinTx(params: {
    userPubkey: string;
    matchId: string;
    opponentMint: string;
  }) {
    const opponent = new PublicKey(params.userPubkey);
    const opponentMint = new PublicKey(params.opponentMint);
    const pid = this.program.programId as PublicKey;

    const matchIdBig = BigInt(params.matchId);
    const matchAccount = matchPda(pid, matchIdBig);
    const opponentTokenAccount = ataAddress(opponentMint, opponent);
    const escrowOpponent = ataAddress(opponentMint, matchAccount);
    const cardMetaOpponent = cardMetaPda(pid, opponentMint);

    const ataIx = await this.maybeCreateAtaIx(
      opponent,
      opponentMint,
      opponentTokenAccount,
      opponent,
    );

    const joinAnchorTx: Transaction = await this.program.methods
      .joinMatch(new anchor.BN(params.matchId))
      .accounts({
        opponent,
        matchAccount,
        opponentMint,
        opponentTokenAccount,
        cardMetaOpponent,
        escrowOpponent,
        tokenProgram: TOKEN_PROGRAM_ID,
        associatedTokenProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
        systemProgram: SystemProgram.programId,
      })
      .transaction();

    const tx = new Transaction();
    if (ataIx) tx.add(ataIx);
    joinAnchorTx.instructions.forEach((ix) => tx.add(ix));

    const finalized = await this.finalizeTx(tx, opponent);

    return {
      tx: finalized
        .serialize({ requireAllSignatures: false })
        .toString('base64'),
      matchAccount: matchAccount.toBase58(),
      escrowOpponent: escrowOpponent.toBase58(),
      opponentTokenAccount: opponentTokenAccount.toBase58(),
      note: 'Подпиши и отправь транзакцию кошельком оппонента.',
    };
  }

  async buildResolveTx(params: { userPubkey: string; matchId: string }) {
    const resolver = new PublicKey(params.userPubkey);
    const pid = this.program.programId as PublicKey;
    const matchIdBig = BigInt(params.matchId);
    const matchAccount = matchPda(pid, matchIdBig);

    // состояние матча
    const m = await this.program.account.matchAccount.fetch(matchAccount);

    const creator = new PublicKey(m.creator);
    const opponent = new PublicKey(m.opponent);
    const creatorMint = new PublicKey(m.creatorMint);
    const opponentMint = new PublicKey(m.opponentMint);

    const escrowCreator = ataAddress(creatorMint, matchAccount);
    const escrowOpponent = ataAddress(opponentMint, matchAccount);

    const creatorDstCreatorMint = ataAddress(creatorMint, creator);
    const creatorDstOpponentMint = ataAddress(opponentMint, creator);
    const opponentDstCreatorMint = ataAddress(creatorMint, opponent);
    const opponentDstOpponentMint = ataAddress(opponentMint, opponent);

    const tx = await this.program.methods
      .resolveMatch(new anchor.BN(params.matchId))
      .accounts({
        resolver,
        matchAccount,
        escrowCreator,
        escrowOpponent,
        creatorDstCreatorMint,
        creatorDstOpponentMint,
        opponentDstCreatorMint,
        opponentDstOpponentMint,
        creator,
        opponent,
        creatorMint,        
        opponentMint,      
        tokenProgram: TOKEN_PROGRAM_ID,
        associatedTokenProgram: ASSOCIATED_TOKEN_PROGRAM_ID,
        systemProgram: SystemProgram.programId,
      })
      .transaction();

    const finalized = await this.finalizeTx(tx, resolver);

    return {
      tx: finalized.serialize({ requireAllSignatures: false }).toString('base64'),
      matchAccount: matchAccount.toBase58(),
    };
  }

  async getMatchState(matchId: string) {
    const pid = this.program.programId as PublicKey;
    const pda = matchPda(pid, BigInt(matchId));
    const acc = await this.program.account.matchAccount.fetch(pda);

    const statusNum: number = acc.status;
    const status =
      statusNum === STATUS_OPEN
        ? 'OPEN'
        : statusNum === STATUS_ACTIVE
          ? 'ACTIVE'
          : statusNum === STATUS_FINISHED
            ? 'FINISHED'
            : `UNKNOWN(${statusNum})`;

    return {
      matchAccount: pda.toBase58(),
      matchId,
      bump: acc.bump,
      status,
      creator: new PublicKey(acc.creator).toBase58(),
      opponent: new PublicKey(acc.opponent).toBase58(),
      creatorMint: new PublicKey(acc.creatorMint).toBase58(),
      opponentMint: new PublicKey(acc.opponentMint).toBase58(),
      creatorCardType: acc.creatorCardType,
      opponentCardType: acc.opponentCardType,
    };
  }

  async listOpenMatches() {
    const now = Date.now();

    if (this.cache.length > 0 && now - this.lastFetch < this.CACHE_TTL) {
      console.log(`КЭШ: ${this.cache.length} открытых матчей (возраст ${(now - this.lastFetch) / 1000}с)`);
      return this.cache;
    }

    try {
      const pid = this.program.programId as PublicKey;

      const statusOffset = 17;
      const openByte = anchor.utils.bytes.bs58.encode(Uint8Array.from([STATUS_OPEN]));

      const accounts = await this.program.account.matchAccount.all([
        { memcmp: { offset: statusOffset, bytes: openByte } },
        { dataSize: 156 },
      ]);

      const result = accounts.map(acc => {
        const a = acc.account;
        const creatorShort = a.creator.toBase58().slice(0, 8) + '...';
        const cardName = ['Rock', 'Paper', 'Scissors'][a.creatorCardType] || 'Unknown';

        return {
          matchId: a.matchId.toString(),
          creator: a.creator.toBase58(),
          creatorShort,
          creatorMint: a.creatorMint.toBase58(),
          card: cardName,
          cardType: a.creatorCardType,
        };
      });

      this.cache = result;
      this.lastFetch = now;

      console.log(`ЗАГРУЖЕНО ${result.length} открытых матчей (кэш обновлён)`);
      return result;

    } catch (error: any) {
      console.error('Ошибка listOpenMatches:', error.message);
      return this.cache;
    }
  }
}
