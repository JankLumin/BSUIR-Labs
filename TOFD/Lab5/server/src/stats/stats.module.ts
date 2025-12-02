import { Module } from '@nestjs/common';
import { StatsController } from './stats.controller';
import { StatsService } from './stats.service';
import { AnchorModule } from '../anchor/anchor.module';

@Module({
  imports: [AnchorModule],
  controllers: [StatsController],
  providers: [
    {
      provide: StatsService,
      useFactory: (program: any) => new StatsService(program),
      inject: ['PROGRAM'],
    },
  ],
})
export class StatsModule {}