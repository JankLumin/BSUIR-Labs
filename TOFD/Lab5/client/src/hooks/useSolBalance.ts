import { useState, useEffect } from 'react';
import { PublicKey, Connection } from '@solana/web3.js';

const connection = new Connection('https://api.devnet.solana.com', 'confirmed');

export function useSolBalance(wallet: PublicKey | null) {
  const [balance, setBalance] = useState<number | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!wallet) {
      setBalance(null);
      setLoading(false);
      return;
    }

    let active = true;
    let interval: ReturnType<typeof setInterval>;

    const fetchBalance = async () => {
      try {
        const lamports = await connection.getBalance(wallet);
        if (active) {
          setBalance(lamports / 1e9);
          setLoading(false);
        }
      } catch (err) {
        console.error('Failed to fetch SOL balance:', err);
        if (active) setLoading(false);
      }
    };

    fetchBalance();
    interval = setInterval(fetchBalance, 30_000); // каждые 30 сек

    return () => {
      active = false;
      clearInterval(interval);
    };
  }, [wallet]);

  return { balance, loading };
}