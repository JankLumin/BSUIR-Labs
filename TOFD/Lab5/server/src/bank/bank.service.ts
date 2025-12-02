import * as anchor from '@coral-xyz/anchor';
import { PublicKey, SystemProgram } from '@solana/web3.js';

function bankStatePda(programId: PublicKey) {
  return PublicKey.findProgramAddressSync(
    [Buffer.from('bank_state')],
    programId,
  )[0];
}
function bankWalletPda(programId: PublicKey) {
  return PublicKey.findProgramAddressSync([Buffer.from('bank')], programId)[0];
}

export class BankService {
  constructor(private readonly program: any) {}

  async initBank() {
    const provider = this.program.provider as anchor.AnchorProvider;
    const admin = (provider.wallet as anchor.Wallet).publicKey;
    const pid = this.program.programId as PublicKey;

    const bankState = bankStatePda(pid);
    const bankWallet = bankWalletPda(pid);

    const sig = await this.program.methods
      .initBank()
      .accounts({
        admin,
        bankState,
        bankWallet,
        systemProgram: SystemProgram.programId,
      })
      .rpc();

    return {
      txid: sig,
      bankState: bankState.toBase58(),
      bankWallet: bankWallet.toBase58(),
      note: 'Пополни bankWallet SOL для ликвидности.',
    };
  }

  async getState() {
    const pid = this.program.programId as PublicKey;
    const bankStatePk = bankStatePda(pid);
    const bankWalletPk = bankWalletPda(pid);
    try {
      const st = await this.program.account.bankState.fetch(bankStatePk);
      return {
        bankState: bankStatePk.toBase58(),
        bankWallet: bankWalletPk.toBase58(),
        admin: (st.admin as PublicKey).toBase58(),
        buyPriceLamports: st.buyPriceLamports.toString(),
        sellPriceLamports: st.sellPriceLamports.toString(),
        bump: st.bump,
      };
    } catch (error) {
      return {
        bankState: bankStatePk.toBase58(),
        bankWallet: bankWalletPk.toBase58(),
        admin: null,
        buyPriceLamports: null,
        sellPriceLamports: null,
        bump: null,
        initialized: false,
        error: 'Bank not initialized',
      };
    }
    
  }

  async updatePrices(buy: string, sell: string) {
    const provider = this.program.provider as anchor.AnchorProvider;
    const admin = (provider.wallet as anchor.Wallet).publicKey;
    const pid = this.program.programId as PublicKey;
    const bankState = bankStatePda(pid);

    const sig = await this.program.methods
      .updatePrices(new anchor.BN(buy), new anchor.BN(sell))
      .accounts({ admin, bankState })
      .rpc();

    return { txid: sig, buyPriceLamports: buy, sellPriceLamports: sell };
  }

  async withdraw(amount: string, to: string) {
    const provider = this.program.provider as anchor.AnchorProvider;
    const admin = (provider.wallet as anchor.Wallet).publicKey;
    const pid = this.program.programId as PublicKey;

    const bankState = bankStatePda(pid);
    const bankWallet = bankWalletPda(pid);

    const sig = await this.program.methods
      .withdraw(new anchor.BN(amount))
      .accounts({
        admin,
        bankState,
        bankWallet,
        to: new PublicKey(to),
        systemProgram: SystemProgram.programId,
      })
      .rpc();

    return { txid: sig, to, amount };
  }
}
