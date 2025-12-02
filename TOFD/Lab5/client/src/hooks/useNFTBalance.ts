import { useState, useEffect } from 'react';
import { PublicKey } from '@solana/web3.js';
import { post } from '../api';  

export function useNFTBalance(wallet: PublicKey | null) {
  const [balance, setBalance] = useState<number>(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!wallet) {
      setBalance(0);
      setLoading(false);
      return;
    }

    let active = true;
    let interval: ReturnType<typeof setInterval>;

    const fetch = async () => {
      try {
        const r = await post<{ inventory: any[] }>('/cards/inventory', {
          userPubkey: wallet.toBase58(),
        });
        if (active) {
          setBalance(r.inventory.length);
          setLoading(false);
        }
      } catch (e) {
        console.error('DNCG balance error:', e);
        if (active) setLoading(false);
      }
    };

    fetch();
    interval = setInterval(fetch, 30_000); // 30 сек

    return () => {
      active = false;
      clearInterval(interval);
    };
  }, [wallet]);

  return { balance, loading };
}