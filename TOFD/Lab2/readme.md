# настройка окружения

solana config set --url https://api.devnet.solana.com
solana config set --keypair ~/.config/solana/id.json

# добавление токенов и проверка баланса

solana airdrop 5
solana balance

# создание токена

spl-token create-token --decimals 6

# записываем токен в переменную

MINT=9MB18qeNRduSfAkWG4zkfxrVNmSGzt3mJoZjaMT458ny

# создаем ATA

spl-token create-account $MINT

# выпускаем токены и проверяем баланс

spl-token mint $MINT 1000000
spl-token balance $MINT
spl-token accounts

# добавляем метаданные и проверяем(записать MINT в .env)

node meta/set-metadata.mjs
node meta/show-metadata.mjs
solana account <Metadata PDA>

# создаем кошельки для airdrop

solana-keygen new --outfile first.json
solana-keygen new --outfile second.json

RECIP1=$(solana-keygen pubkey first.json)
RECIP2=$(solana-keygen pubkey second.json)

# выдача токенов на кошельки

spl-token transfer $MINT 100 $RECIP1 --allow-unfunded-recipient --fund-recipient
spl-token transfer $MINT 250 $RECIP2 --allow-unfunded-recipient --fund-recipient

# проверка балансов

spl-token supply $MINT
spl-token balance $MINT

spl-token accounts --owner $RECIP1
spl-token accounts --owner $RECIP2

---

# конвертируем токены в WSOL и проверяем баланс

spl-token wrap 2
spl-token accounts So11111111111111111111111111111111111111112

# переходим в папку проекта создаем пул и выполняем swap, проверяя балансы(измеинть pool_id в .env)

cd raydium-sdk-V2-demo
npx ts-node src/cpmm/createCpmmPool.ts
spl-token accounts
npx ts-node src/cpmm/swap.ts
spl-token accounts

---

# получаем все цены

npx ts-node src/price/pyth.ts
