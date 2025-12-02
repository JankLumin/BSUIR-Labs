import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Dashboard.css';

interface Stats {
  wins: number;
  losses: number;
  draws: number;
  winrate: number;
  totalGames: number;
  history: { matchId: string; myCard: string; opponentCard: string; outcome: 'WIN'|'LOSS'|'DRAW'; ago: string }[];
}

export default function Dashboard({ wallet }: { wallet: any }) {
  const navigate = useNavigate();
  const [stats, setStats] = useState<Stats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (!wallet) return;

    const load = async () => {
      try {
        const res = await fetch('http://localhost:3000/stats', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userPubkey: wallet.toBase58() }),
        });
        const data = await res.json();
        setStats(data.stats);
      } catch (err) {
        console.error('Stats load failed');
      } finally {
        setLoading(false);
      }
    };

    load();
    const id = setInterval(load, 12000);
    return () => clearInterval(id);
  }, [wallet]);

  if (!wallet) return <div>Connect wallet</div>;

  const recent = stats?.history.slice(0, 5) || [];

  return (
    <div className="dashboard-grid">
      {/* Quick Actions */}
      <aside className="quick-actions">
        <h3>Quick Actions</h3>
        <button onClick={() => navigate('/bank')} className="action-btn bank-btn">Bank</button>
        <button onClick={() => navigate('/lobby')} className="action-btn lobby-btn">Lobby</button>
        <button onClick={() => navigate('/inventory')} className="action-btn inventory-btn">Inventory</button>
      </aside>

      <main className="match-carousel">
        <h3>Recent Matches</h3>
        {loading ? <p>Loading...</p> : recent.length === 0 ? <p>No matches yet</p> : (
          <div className="carousel">
            {recent.map((m, i) => (
              <div key={i} className="carousel-item">
                <div className={`match-card outcome-${m.outcome.toLowerCase()}`}>
                  <h4>Match #{m.matchId}</h4>
                  <p>{m.myCard} vs {m.opponentCard}</p>
                  <span className="outcome">{m.outcome}</span>
                  <small>{m.ago}</small>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>

      {/* Stats */}
      <aside className="stats-panel">
        <h3>Your Stats</h3>
        {stats && (
          <>
            <div className="winrate-circle" style={{
              background: `conic-gradient(#10b981 0% ${stats.winrate}%, #334155 ${stats.winrate}% 100%)`
            }}>
              <span>{stats.winrate}%</span>
            </div>
            <div className="stats-numbers">
              <div><strong>{stats.wins}</strong> Wins</div>
              <div><strong>{stats.losses}</strong> Losses</div>
              <div><strong>{stats.draws}</strong> Draws</div>
            </div>
            <p style={{ textAlign: 'center', marginTop: '1rem', opacity: 0.8 }}>
              Total: <strong>{stats.totalGames}</strong> games
            </p>
          </>
        )}
      </aside>
    </div>
  );
}