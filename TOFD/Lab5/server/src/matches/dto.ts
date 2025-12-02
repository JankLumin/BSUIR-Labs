import { ApiProperty } from '@nestjs/swagger';
import { IsNotEmpty, IsNumberString, IsString } from 'class-validator';

export class BuildCreateMatchDto {
  @ApiProperty() @IsString() @IsNotEmpty() userPubkey!: string;
  @ApiProperty({ example: '1' }) @IsNumberString() matchId!: string;
  @ApiProperty() @IsString() @IsNotEmpty() creatorMint!: string;
}

export class BuildJoinMatchDto {
  @ApiProperty() @IsString() @IsNotEmpty() userPubkey!: string;
  @ApiProperty({ example: '1' }) @IsNumberString() matchId!: string;
  @ApiProperty() @IsString() @IsNotEmpty() opponentMint!: string;
}

export class BuildResolveMatchDto {
  @ApiProperty() @IsString() @IsNotEmpty() userPubkey!: string; 
  @ApiProperty({ example: '1' }) @IsNumberString() matchId!: string;
}
