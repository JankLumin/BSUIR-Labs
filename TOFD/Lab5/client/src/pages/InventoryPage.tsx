import { useState, useEffect } from 'react';
import { PublicKey } from '@solana/web3.js';
import { post } from '../api';
import { useNavigate } from 'react-router-dom';
import './InventoryPage.css';

interface Card {
  mint: string;
  name: string;
  symbol: string;
  uri: string;
  cardType: number;
  mintTime: string;
}

interface InventoryProps {
  wallet: PublicKey | null;
}

export default function Inventory({ wallet }: InventoryProps) {
  const [cards, setCards] = useState<Card[]>([]);
  const [loading, setLoading] = useState(true);
  const [copiedMint, setCopiedMint] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    if (!wallet) return;
    loadInventory();
  }, [wallet]);

  const loadInventory = async () => {
    if (!wallet) return;
    try {
      setLoading(true);
      const r = await post<{ inventory: Card[] }>('/cards/inventory', {
        userPubkey: wallet.toBase58(),
      });
      setCards(r.inventory);
    } catch (e: any) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const copyMint = async (mint: string) => {
    try {
      await navigator.clipboard.writeText(mint);
      setCopiedMint(mint);
      setTimeout(() => setCopiedMint(null), 2000); // 2 сек
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  if (!wallet) {
    return <div className="page-container">Connect wallet to view inventory</div>;
  }

  return (
    <div className="page-container">
      <div className="inventory-header">
        <h2>My Cards ({cards.length})</h2>
      </div>
      <div>
        <button onClick={() => navigate('/bank')} className="action-btn">
          Back to Bank
        </button>
      </div>

      {loading ? (
        <p>Loading cards...</p>
      ) : cards.length === 0 ? (
        <p>No cards yet. Go to <strong>Bank</strong> and mint one!</p>
      ) : (
        <div className="inventory-grid">
          {cards.map((card) => (
            <div key={card.mint} className="nft-card">
              {card.uri ? (
                <img src={card.uri} alt={card.name} className="nft-image" />
              ) : (
                <div className="nft-placeholder">
                  <span>{card.symbol}</span>
                </div>
              )}
              <div className="nft-info">
                <h4>{card.name}</h4>
                <p>Type: {['Rock', 'Paper', 'Scissors'][card.cardType] || 'Unknown'}</p>
                <small>Minted: {card.mintTime}</small>
                <br/>
                <a
                  href={`https://explorer.solana.com/address/${card.mint}?cluster=devnet`}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="explorer-link"
                >
                  View on Explorer
                </a>
                <button
                    onClick={() => copyMint(card.mint)}
                    className="copy-mint-btn"
                    title="Copy mint address"
                >
                    {copiedMint === card.mint ? (
                      <span className="copied-text">Copied!</span>
                    ) : (
                      <svg
                        xmlns="http://www.w3.org/2000/svg"
                        width="16"
                        height="16"
                        fill="currentColor"
                        viewBox="0 0 16 16"
                      >
                        <path d="M4 1.5H3a2 2 0 0 0-2 2V14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V3.5a2 2 0 0 0-2-2h-1v1h1a1 1 0 0 1 1 1V14a1 1 0 0 1-1 1H3a1 1 0 0 1-1-1V3.5a1 1 0 0 1 1-1h1v-1z"/>
                        <path d="M9.5 1a.5.5 0 0 1 .5-.5h2.5a.5.5 0 0 1 0 1h-2.5a.5.5 0 0 1-.5-.5z"/>
                        <path d="M8.5 1h-2a.5.5 0 0 0 0 1h2a.5.5 0 0 0 0-1z"/>
                      </svg>
                    )}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}