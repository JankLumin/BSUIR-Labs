// src/App.tsx
import { useState, useEffect } from 'react';
import { Routes, Route, useNavigate } from 'react-router-dom';
import SplashScreen from './components/SplashScreen';
import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import BankPage from './pages/BankPage';
import LobbyPage from './pages/LobbyPage';
import Inventory from './pages/InventoryPage';
import { PublicKey } from '@solana/web3.js';

declare global { interface Window { solana?: any } }

export default function App() {
  const [wallet, setWallet] = useState<PublicKey | null>(null);
  const [showSplash, setShowSplash] = useState(true);
  const [isFading, setIsFading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const saved = localStorage.getItem('dncg_wallet');
    if (saved) {
      setWallet(new PublicKey(saved));
      setShowSplash(false);
    }
  }, []);

  const connectWallet = async () => {
    const provider = window.solana;
    if (!provider?.isPhantom) {
      alert('Install Phantom: https://phantom.app');
      return;
    }
    try {
      const resp = await provider.connect();
      const pubkey = new PublicKey(resp.publicKey.toString());
      setWallet(pubkey);
      localStorage.setItem('dncg_wallet', pubkey.toBase58());
    } catch (err) {
      console.error(err);
    }
  };

  const goToDashboard = () => {
    setIsFading(true);
    setTimeout(() => {
      setShowSplash(false);
      navigate('/');
    }, 800);
  };

  const disconnect = () => {
    setWallet(null);
    localStorage.removeItem('dncg_wallet');
    navigate('/');
  };

  if (showSplash) {
    return (
      <div className={isFading ? 'splash-fade-out' : ''}>
        <SplashScreen
          wallet={wallet}
          onConnect={connectWallet}
          onNext={goToDashboard}
        />
      </div>
    );
  }

  return (
    <Layout wallet={wallet} onDisconnect={disconnect}>
      <Routes>
        <Route path="/" element={<Dashboard wallet={wallet} />} />
        <Route path="/bank" element={<BankPage wallet={wallet} />} />
        <Route path="/lobby" element={<LobbyPage wallet={wallet} />} />
        <Route path="/inventory" element={<Inventory wallet={wallet} />}/>
      </Routes>
    </Layout>
  );
}