import { ApiProperty } from '@nestjs/swagger';
import { IsNumberString, IsString } from 'class-validator';

export class UpdatePricesDto {
  @ApiProperty({ example: '100000000' }) @IsNumberString() buy!: string; 
  @ApiProperty({ example: '90000000' }) @IsNumberString() sell!: string;
}

export class WithdrawDto {
  @ApiProperty() @IsString() to!: string;
  @ApiProperty({ example: '100000000' }) @IsNumberString() amount!: string;
}
