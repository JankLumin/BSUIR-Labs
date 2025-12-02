import { Module } from '@nestjs/common';
import { AnchorModule } from './anchor/anchor.module';
import { BankModule } from './bank/bank.module';
import { MintModule } from './mint/mint.module';
import { MatchesModule } from './matches/matches.module';
import { StatsModule } from './stats/stats.module';

@Module({
  imports: [AnchorModule, BankModule, MintModule, MatchesModule, StatsModule],
})
export class AppModule {}
