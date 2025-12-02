import { Module } from '@nestjs/common';
import { BankController } from './bank.controller';
import { BankService } from './bank.service';
import { AnchorModule } from '../anchor/anchor.module';

@Module({
  imports: [AnchorModule],
  controllers: [BankController],
  providers: [
    {
      provide: BankService,
      useFactory: (program) => new BankService(program),
      inject: ['PROGRAM'],
    },
  ],
})
export class BankModule {}
