import { useState } from 'react';
import { PublicKey } from '@solana/web3.js';
import { post } from '../api';
import { signAndSendRaw, txFromBase64 } from '../tx';
import { Connection } from '@solana/web3.js';
import { SendTransactionError } from '@solana/web3.js';
import './BankPage.css'

interface BankPageProps {
  wallet: PublicKey | null;
}

export default function BankPage({ wallet }: BankPageProps) {
  const [cardType, setCardType] = useState(0);
  const [name, setName] = useState('Rock');
  const [symbol, setSymbol] = useState('DNCG');
  const [uri, setUri] = useState('https://example.com/metadata.json');
  const [sellMint, setSellMint] = useState('');
  const [log, setLog] = useState<string[]>([]);
  const add = (s: string) => setLog(l => [`${new Date().toLocaleTimeString()} ${s}`, ...l]);

  const conn = new Connection('https://api.devnet.solana.com', 'confirmed');
  const provider = typeof window !== 'undefined' ? window.solana : null;

  const sendTx = async (txBase64: string, action: string) => {
    const tx = txFromBase64(txBase64);
    try {
      const sig = await signAndSendRaw(conn, provider!, tx);
      add(`${action} sig: ${sig}`);
      return sig;
    } catch (e: any) {
      if (e instanceof SendTransactionError) {
        const logs = await e.getLogs(conn);
        add(`TRANSACTION FAILED: ${action}`);
        add(`Signature: ${(e as any).signature || 'unknown'}`);
        add(`Error: ${e.message}`);
        add('--- FULL LOGS ---');
        logs.forEach((log) => add(log));
        add('--- END LOGS ---');
      } else {
        add(`Error (${action}): ${e.message}`);
        console.error(e);
      }
      throw e;
    }
  };

  const onMint = async () => {
    if (!wallet || !provider) return alert('Connect wallet');
    try {
      const userPubkey = wallet.toBase58();
      console.log('userPubkey:', userPubkey);
      const r = await post<any>('/cards/mint/build-tx', {
        userPubkey: userPubkey, cardType, name, symbol, uri
      });
      await sendTx(r.tx, 'Mint');
      add(`Minted NFT: ${r.mint}`)
      // const sig = await signAndSendRaw(conn, provider, txFromBase64(r.tx));
      // add(`Mint sig: ${sig}`);
    } catch (e: any) { 
      console.error(e);
      add(`Error: ${e.message}`); 
    }
  };

  const onSell = async () => {
    if (!wallet || !provider || !sellMint) return;
    try {
      add(`Selling NFT ${sellMint}...`);
      const r = await post<any>('/cards/sell/build-tx', {
        userPubkey: wallet.toBase58(), mint: sellMint
      });
      add(`Bank will pay: ${r.sellPrice || '90_000_000'} lamports`);
      add(`Token Account: ${r.tokenAccount}`);
      add(`CardMeta: ${r.cardMeta}`);
      await sendTx(r.tx, 'Sell');
      // const sig = await signAndSendRaw(conn, provider, txFromBase64(r.tx));
      // add(`Sell sig: ${sig}`);
    } catch (e: any) { add(`Error: ${e.message}`); }
  };

  const onGetBank = async () => {
    try {
      const state = await fetch('/bank/state').then(r => r.json());

      if (state.error || !state.initialized) {
        add('Bank not initialized');
        add(`bankState PDA: ${state.bankState}`);
        add(`bankWallet PDA: ${state.bankWallet}`);
        add('Call POST /bank/init first');
        return;
      }

      add(`Bank Admin: ${state.admin}`);
      add(`Buy Price: ${state.buyPriceLamports} lamports`);
      add(`Sell Price: ${state.sellPriceLamports} lamports`);
      add(`Bank Wallet: ${state.bankWallet}`);
    } catch (e: any) {
      add(`Network error: ${e.message}`);
    }
  };

  return (
    <div className="page-container">
      <h2>Bank</h2>
      <div className="modal-content">
        <h4>Mint Card</h4>
        <div className="card-type-selector">
          <span className="selector-label">Card Type:</span>
          <div className="type-buttons">
            {['Rock', 'Paper', 'Scissors'].map((type, index) => (
              <button
                key={index}
                onClick={() => {
                  setCardType(index);
                  setName(type);
                }}
                className={cardType === index ? 'active' : ''}
              >
                {type}
              </button>
            ))}
          </div>
        </div>
        <input
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="name (можно изменить)"
          style={{ marginTop: '0.75rem' }}
        />

        <input
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="symbol (обычно DNCG)"
          style={{ marginTop: '0.5rem' }}
        />

        <input
          value={uri}
          onChange={(e) => setUri(e.target.value)}
          placeholder="uri (метаданные)"
          style={{ width: '100%', marginTop: '0.5rem' }}
        />

        <button onClick={onMint} disabled={!wallet} style={{ marginTop: '1rem' }}>
          Mint {name || 'Card'}
        </button>

        <h4 style={{ marginTop: '1.5rem' }}>Sell to Bank</h4>
        <input value={sellMint} onChange={e => setSellMint(e.target.value)} placeholder="mint" style={{ width: '100%' }} />
        <button onClick={onSell} disabled={!wallet || !sellMint}>Sell</button>
        <button onClick={onGetBank} className="get-bank-btn">Get Bank State</button>
      </div>

      <div className="log-section" style={{ marginTop: '2rem' }}>
        <h4>Log</h4>
        <pre className="log-box">{log.join('\n')}</pre>
      </div>
    </div>
  );
}