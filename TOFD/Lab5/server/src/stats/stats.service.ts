import { Injectable } from '@nestjs/common';
import { PublicKey } from '@solana/web3.js';
import * as anchor from '@coral-xyz/anchor';

const ZERO_PUBKEY = new PublicKey(0);

@Injectable()
export class StatsService {
  constructor(private readonly program: any) {}

  async getPlayerStats(wallet: PublicKey) {
    try {
      // Размер MatchAccount = 156 байт
      const allMatches = await this.program.account.matchAccount.all([
        {
          dataSize: 156,
        },
      ]);

      console.log('Найдено матчей с правильным размером:', allMatches.length);

      const myMatches = allMatches
        .filter(m => 
          m.account.creator.equals(wallet) || 
          (!m.account.opponent.equals(ZERO_PUBKEY) && m.account.opponent.equals(wallet))
        )
        .filter(m => m.account.status === 2); // STATUS_FINISHED

      const stats = { wins: 0, losses: 0, draws: 0, history: [] as any[] };

      for (const m of myMatches) {
        const isCreator = m.account.creator.equals(wallet);
        
        const myType = isCreator ? m.account.creatorCardType : m.account.opponentCardType;
        const oppType = isCreator ? m.account.opponentCardType : m.account.creatorCardType;

        const outcome = ((myType - oppType + 3) % 3);
        const result = outcome === 0 ? 'DRAW' : outcome === 1 ? 'WIN' : 'LOSS';

        if (result === 'WIN') stats.wins++;
        else if (result === 'LOSS') stats.losses++;
        else stats.draws++;

        const opponent = isCreator ? m.account.opponent : m.account.creator;
        const opponentStr = opponent.equals(ZERO_PUBKEY)
          ? 'unknown'
          : opponent.toBase58().slice(0, 8) + '...';

        const ts = m.account.timestamp?.toNumber() || 0;
        const ago = ts === 0 ? 'long ago' : this.timeAgo(ts * 1000);

        stats.history.push({
          matchId: m.account.matchId.toString(), 
          opponent: opponentStr,
          myCard: ['Rock', 'Paper', 'Scissors'][myType] ?? 'Unknown',
          opponentCard: ['Rock', 'Paper', 'Scissors'][oppType] ?? 'Unknown',
          outcome: result,
          ago,
        });
      }

      stats.history.sort((a, b) => {
          return 0; 
      });
      
      stats.history.reverse();

      const total = stats.wins + stats.losses + stats.draws;
      const winrate = total > 0 ? Math.round((stats.wins / total) * 100) : 0;

      return {
        wins: stats.wins,
        losses: stats.losses,
        draws: stats.draws,
        winrate,
        totalGames: total,
        history: stats.history,
      };
    } catch (error) {
      console.error('Ошибка в getPlayerStats:', error);
      return {
        wins: 0,
        losses: 0,
        draws: 0,
        winrate: 0,
        totalGames: 0,
        history: [],
        error: error.message,
      };
    }
  }

  private timeAgo(ts: number): string {
    const seconds = Math.floor((Date.now() - ts) / 1000);
    if (seconds < 60) return 'just now';
    if (seconds < 3600) return `${Math.floor(seconds / 60)} min ago`;
    if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`;
    return `${Math.floor(seconds / 86400)}d ago`;
  }
}