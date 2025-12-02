import { Body, Controller, Post } from '@nestjs/common';
import { ApiTags } from '@nestjs/swagger';
import { StatsService } from './stats.service';
import { PublicKey } from '@solana/web3.js';

@ApiTags('stats')
@Controller('stats')
export class StatsController {
  constructor(private readonly statsService: StatsService) {}

  @Post()
  async getStats(@Body('userPubkey') userPubkey: string) {
    if (!userPubkey) throw new Error('userPubkey required');
    const stats = await this.statsService.getPlayerStats(new PublicKey(userPubkey));
    return { stats };
  }
}