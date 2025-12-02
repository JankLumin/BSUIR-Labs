import { Body, Controller, Get, Post } from '@nestjs/common';
import { ApiTags } from '@nestjs/swagger';
import { BankService } from './bank.service';
import { UpdatePricesDto, WithdrawDto } from './dto';

@ApiTags('bank')
@Controller('bank')
export class BankController {
  constructor(private readonly svc: BankService) {}

  @Post('init')
  init() {
    return this.svc.initBank();
  }

  @Get('state')
  state() {
    return this.svc.getState();
  }

  @Post('update-prices')
  update(@Body() dto: UpdatePricesDto) {
    return this.svc.updatePrices(dto.buy, dto.sell);
  }

  @Post('withdraw')
  withdraw(@Body() dto: WithdrawDto) {
    return this.svc.withdraw(dto.amount, dto.to);
  }
}
