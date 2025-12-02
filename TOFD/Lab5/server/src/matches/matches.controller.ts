import { Body, Controller, Get, Param, Post } from '@nestjs/common';
import { ApiTags } from '@nestjs/swagger';
import { MatchesService } from './matches.service';
import {
  BuildCreateMatchDto,
  BuildJoinMatchDto,
  BuildResolveMatchDto,
} from './dto';

@ApiTags('matches')
@Controller('matches')
export class MatchesController {
  constructor(private readonly svc: MatchesService) {}

  @Post('create/build-tx')
  buildCreate(@Body() dto: BuildCreateMatchDto) {
    return this.svc.buildCreateTx({
      userPubkey: dto.userPubkey,
      matchId: dto.matchId,
      creatorMint: dto.creatorMint,
    });
  }

  @Post('join/build-tx')
  buildJoin(@Body() dto: BuildJoinMatchDto) {
    return this.svc.buildJoinTx({
      userPubkey: dto.userPubkey,
      matchId: dto.matchId,
      opponentMint: dto.opponentMint,
    });
  }

  @Post('resolve/build-tx')
  buildResolve(@Body() dto: BuildResolveMatchDto) {
    return this.svc.buildResolveTx({
      userPubkey: dto.userPubkey,
      matchId: dto.matchId,
    });
  }

  @Get('open')
  listOpen() {
    return this.svc.listOpenMatches();
  }

  @Get(':matchId/state')
  state(@Param('matchId') matchId: string) {
    return this.svc.getMatchState(matchId);
  }
}
