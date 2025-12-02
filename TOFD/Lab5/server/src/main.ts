import 'dotenv/config';
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

async function bootstrap() {
  const app = await NestFactory.create(AppModule, { cors: true });

  const cfg = new DocumentBuilder()
    .setTitle('DNCG API')
    .setDescription('Backend for Decentralized NFT Card Game')
    .setVersion('1.0.0')
    .build();
  const doc = SwaggerModule.createDocument(app, cfg);
  SwaggerModule.setup('/docs', app, doc);

  await app.listen(3000);
  console.log('Swagger: http://localhost:3000/docs');
}
bootstrap();
