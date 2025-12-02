// src/pages/LobbyPage.tsx
import { useEffect, useState } from 'react';
import { PublicKey } from '@solana/web3.js';
import { post } from '../api';
import { signAndSendRaw, txFromBase64 } from '../tx';
import { Connection } from '@solana/web3.js';
import './LobbyPage.css';

interface OpenMatch {
  matchId: string;
  creatorShort: string;
  creatorMint: string;
  card: 'Rock' | 'Paper' | 'Scissors';
}

interface LobbyPageProps {
  wallet: PublicKey | null;
}

export default function LobbyPage({ wallet }: LobbyPageProps) {
  const [openMatches, setOpenMatches] = useState<OpenMatch[]>([]);
  const [myMint, setMyMint] = useState('');
  const [createMint, setCreateMint] = useState('');
  const [resolveMatchId, setResolveMatchId] = useState('');
  const [loading, setLoading] = useState(true);
  const [creating, setCreating] = useState(false);

  const conn = new Connection('https://api.devnet.solana.com', 'confirmed');
  const provider = typeof window !== 'undefined' ? window.solana : null;

  const loadMatches = async () => {
    try {
      const res = await fetch('http://localhost:3000/matches/open');
      const data = await res.json();
      setOpenMatches(data);
    } catch (err) {
      console.error('Не удалось загрузить матчи');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadMatches();
  }, []);

  const createMatch = async () => {
    if (!wallet || !provider || !createMint.trim()) return;
    setCreating(true);
    try {
      const matchId = Date.now().toString().slice(-6);
      const r = await post<{ tx: string }>('/matches/create/build-tx', {
        userPubkey: wallet.toBase58(),
        matchId,
        creatorMint: createMint.trim(),
      });
      const sig = await signAndSendRaw(conn, provider, txFromBase64(r.tx));
      alert(`Матч #${matchId} создан! Подтверждение: ${sig.slice(0, 8)}…${sig.slice(-4)}`);
      setCreateMint('');
      loadMatches();
    } catch (e: any) {
      alert('Ошибка создания матча: ' + (e.message || 'Неизвестная ошибка'));
    } finally {
      setCreating(false);
    }
  };

  const joinMatch = async (matchId: string) => {
    if (!wallet || !provider || !myMint.trim()) {
      alert('Введи mint своей NFT!');
      return;
    }
    try {
      const r = await post<{ tx: string }>('/matches/join/build-tx', {
        userPubkey: wallet.toBase58(),
        matchId,
        opponentMint: myMint.trim(),
      });
      const sig = await signAndSendRaw(conn, provider, txFromBase64(r.tx));
      alert(`ТЫ В МАТЧЕ #${matchId}!\nПодтверждение: ${sig.slice(0, 8)}…${sig.slice(-4)}`);
      loadMatches();
    } catch (e: any) {
      alert('Ошибка входа: ' + (e.message || 'Неизвестная ошибка'));
    }
  };

  const resolveMatch = async () => {
    if (!wallet || !provider) return;
    const id = resolveMatchId.trim();
    if (!id) {
      alert('Введи ID матча для расчёта');
      return;
    }

    try {
      const r = await post<{ tx: string }>('/matches/resolve/build-tx', {
        userPubkey: wallet.toBase58(),
        matchId: id,
      });
      const sig = await signAndSendRaw(conn, provider, txFromBase64(r.tx));
      alert(`МАТЧ #${id} УСПЕШНО ЗАВЕРШЁН!\nПриз отправлен победителю!\nПодпись: ${sig.slice(0, 8)}…`);
      setResolveMatchId('');
      loadMatches();
    } catch (e: any) {
      alert('Ошибка завершения матча:\n' + (e.message || 'Неизвестная ошибка'));
    }
  };

  const cardEmoji = (card: string) => {
    return card === 'Rock' ? 'Rock' : card === 'Paper' ? 'Paper' : 'Scissors';
  };

  return (
    <div className="lobby-bg">
      <div className="lobby-container">
        <h1 className="lobby-title">Rock Paper Scissors Arena</h1>

        {/* Создать матч */}
        <div className="create-section glass">
          <h2>Создать матч</h2>
          <div className="input-group">
            <input
              placeholder="Mint твоей NFT (например, 7xKj...)"
              value={createMint}
              onChange={(e) => setCreateMint(e.target.value)}
            />
            <button onClick={createMatch} disabled={creating || !createMint || !wallet}>
              {creating ? 'Создаём...' : 'Создать матч'}
            </button>
          </div>
        </div>

        <div className="my-mint glass">
          <input
            placeholder="Твой mint для входа в матчи"
            value={myMint}
            onChange={(e) => setMyMint(e.target.value)}
          />
        </div>

        </div>

        <div className="resolve-section glass" style={{ margin: '2rem 0' }}>
          <h2>Завершить матч</h2>
          <div className="input-group">
            <input
              placeholder="ID матча для расчёта (например: 987654)"
              value={resolveMatchId}
              onChange={(e) => setResolveMatchId(e.target.value)}
            />
            <button
              className="resolve-big-btn"
              onClick={resolveMatch}
              disabled={!wallet || !resolveMatchId.trim()}
            >
              РАССЧИТАТЬ РЕЗУЛЬТАТ
            </button>
          </div>
        </div>

        {/* Список открытых матчей */}
        <div className="matches-section">
          <div className="header">
            <h2>Открытые матчи ({openMatches.length})</h2>
            <button onClick={loadMatches} className="refresh-btn">
              Обновить
            </button>
          </div>

          {loading ? (
            <p className="status">Загрузка матчей...</p>
          ) : openMatches.length === 0 ? (
            <p className="status">Пока нет открытых матчей. Будь первым!</p>
          ) : (
            <div className="matches-grid">
              {openMatches.map((m) => (
                <div key={m.matchId} className="match-card glass">
                  <div className="match-id">#{m.matchId}</div>
                  <div className="creator">
                    <span>Создатель:</span> {m.creatorShort}
                  </div>
                  {/* <div className={`card-display ${m.card.toLowerCase()}`}>
                    {cardEmoji(m.card)} {m.card}
                  </div> */}
                  <button
                    className="join-btn"
                    onClick={() => joinMatch(m.matchId)}
                    disabled={!myMint || !wallet}
                  >
                    ВОЙТИ В МАТЧ
                  </button>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
  );
}