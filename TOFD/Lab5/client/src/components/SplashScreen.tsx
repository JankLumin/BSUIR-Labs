import { useState, useEffect } from 'react';
import { PublicKey } from '@solana/web3.js';
import '../splash.css';

interface SplashScreenProps {
  wallet: PublicKey | null;
  onConnect: () => void;
  onNext: () => void;
}

export default function SplashScreen({ wallet, onConnect, onNext }: SplashScreenProps) {
  const [progress, setProgress] = useState(0);
  const [showButtons, setShowButtons] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(p => {
        if (p >= 100) {
          clearInterval(interval);
          setTimeout(() => setShowButtons(true), 400);
          return 100;
        }
        return p + 1.8;
      });
    }, 45);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="splash-container">
      {/* Фоновые карты */}
      <div className="splash-cards">
        <div className="card-float">Rock</div>
        <div className="card-float">Scissors</div>
        <div className="card-float">Paper</div>
      </div>

      <div className="splash-content">
        <h1 className="splash-logo">DNCG</h1>
        <p className="connecting-text">Connecting to Solana...</p>

        <div className="progress-container">
          <div className="progress-bar" style={{ width: `${progress}%` }} />
        </div>

        {showButtons && (
          <div className="splash-buttons-container">
            {!wallet ? (
              <button
                onClick={onConnect}
                className="splash-btn splash-btn-connect"
              >
                Connect Phantom
              </button>
            ) : (
              <>
                <p className="splash-connected-text">
                  Connected: {wallet.toBase58().slice(0, 8)}...{wallet.toBase58().slice(-4)}
                </p>
                <button
                  onClick={onNext}
                  className="splash-btn splash-btn-next"
                >
                  Next
                </button>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}