import type { ReactNode } from 'react';
import { PublicKey } from '@solana/web3.js';
import Particles from './Particles';
import { useNavigate, useLocation } from 'react-router-dom';
import { useSolBalance } from '../hooks/useSolBalance';
import { useNFTBalance } from '../hooks/useNFTBalance';

interface LayoutProps {
  children: ReactNode;
  wallet: PublicKey | null;
  onDisconnect: () => void;
}

export default function Layout({ children, wallet, onDisconnect }: LayoutProps) {
  const navigate = useNavigate();
  const location = useLocation();
  const { balance, loading } = useSolBalance(wallet);
  const { balance: nft, loading: nftLoading } = useNFTBalance(wallet);

  const isDashboard = location.pathname === '/';

  return (
    <div className="dashboard-container">
      <Particles />

      <header className="dashboard-header">
        <div className="header-left">
          {!isDashboard && (
            <button
              onClick={() => navigate('/')}
              className="home-btn"
            >
              Dashboard
            </button>
          )}

          <div className="welcome">
            <h1>Welcome back</h1>
            <p>
              {wallet
                ? `${wallet.toBase58().slice(0, 8)}...${wallet.toBase58().slice(-4)}`
                : 'Guest'}
            </p>
          </div>
        </div>

        <div className="header-right">
          <div className="balances">
            <div className="balance-card">
              <span>SOL</span>
              <strong>
                {loading ? '...' : balance !== null ? balance.toFixed(4) : '0.0000'}
              </strong>
            </div>
            <div className="balance-card">
              <span>Cards:</span>
              <strong>{nftLoading ? '...' : nft}</strong>
            </div>
          </div>

          <button onClick={onDisconnect} className="connect-btn">
            Disconnect
          </button>
        </div>
      </header>

      <main style={{ padding: '0 1rem', flex: 1 }}>
        {children}
      </main>
    </div>
  );
}