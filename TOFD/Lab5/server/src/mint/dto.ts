import { ApiProperty } from '@nestjs/swagger';
import { IsInt, IsNotEmpty, IsString, IsUrl } from 'class-validator';

export class BuildMintDto {
  @ApiProperty() @IsString() @IsNotEmpty() userPubkey!: string;
  @ApiProperty() @IsInt() cardType!: number;
  @ApiProperty() @IsString() @IsNotEmpty() name!: string;
  @ApiProperty() @IsString() @IsNotEmpty() symbol!: string;
  @ApiProperty() @IsUrl() uri!: string;
}

export class BuildSellDto {
  @ApiProperty() @IsString() @IsNotEmpty() userPubkey!: string;
  @ApiProperty() @IsString() @IsNotEmpty() mint!: string;
}
