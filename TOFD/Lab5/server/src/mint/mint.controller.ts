import { Body, Controller, Post } from '@nestjs/common';
import { ApiTags } from '@nestjs/swagger';
import { MintService } from './mint.service';
import { BuildMintDto, BuildSellDto } from './dto';

@ApiTags('cards')
@Controller('cards')
export class MintController {
  constructor(private readonly svc: MintService) {}

  @Post('mint/build-tx')
  build(@Body() dto: BuildMintDto) {
    return this.svc.buildMintTx({
      userPubkey: dto.userPubkey,
      cardType: dto.cardType,
      name: dto.name,
      symbol: dto.symbol,
      uri: dto.uri,
    });
  }

  @Post('sell/build-tx')
  sell(@Body() dto: BuildSellDto) {
    return this.svc.buildSellTx({
      userPubkey: dto.userPubkey,
      mint: dto.mint,
    });
  }

  @Post('inventory')
  async inventory(@Body() dto: { userPubkey: string }) {
    return this.svc.getInventory(dto.userPubkey);
  }
}
