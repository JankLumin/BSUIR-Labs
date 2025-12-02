import { Module } from '@nestjs/common';
import { MatchesController } from './matches.controller';
import { MatchesService } from './matches.service';

@Module({
  controllers: [MatchesController],
  providers: [
    {
      provide: MatchesService,
      useFactory: (conn, program) => new MatchesService(conn, program),
      inject: ['CONNECTION', 'PROGRAM'],
    },
  ],
})
export class MatchesModule {}
