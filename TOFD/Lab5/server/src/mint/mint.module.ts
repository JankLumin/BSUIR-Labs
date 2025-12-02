import { Module } from '@nestjs/common';
import { MintController } from './mint.controller';
import { MintService } from './mint.service';

@Module({
  controllers: [MintController],
  providers: [
    {
      provide: MintService,
      useFactory: (conn, program) => new MintService(conn, program),
      inject: ['CONNECTION', 'PROGRAM'],
    },
  ],
})
export class MintModule {}
