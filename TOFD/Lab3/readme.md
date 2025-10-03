# настройка окружения

solana-test-validator --reset
solana config set --url localhost
solana config set --keypair ~/.config/solana/id.json
MINT=$(spl-token create-token --decimals 6 | awk '/Creating token/ {print $3}')
spl-token create-account $MINT
spl-token mint $MINT 1000000
spl-token balance $MINT
spl-token accounts
solana-keygen new --outfile first.json
solana-keygen new --outfile second.json
RECIP1=$(solana-keygen pubkey first.json)
RECIP2=$(solana-keygen pubkey second.json)
spl-token transfer $MINT 100 $RECIP1 --allow-unfunded-recipient --fund-recipient
spl-token transfer $MINT 250 $RECIP2 --allow-unfunded-recipient --fund-recipient
spl-token supply $MINT
spl-token balance $MINT
spl-token accounts --owner $RECIP1
spl-token accounts --owner $RECIP2
spl-token wrap 2
spl-token accounts So11111111111111111111111111111111111111112
echo "MINT=$MINT"

# компиляция и деплой

cd counter-app
anchor clean
anchor build
anchor deploy

# 3 инкремента и 1 декремент

npx ts-node client/counter.ts
solana account <PUBKEY> --output json \
 | jq -r '.account.data[0]' \
 | base64 -d \
 | od -An -t u8

---

# компиляция и деплой

cd ../dex-app
anchor clean
anchor build
anchor deploy

# скрипт для обменов

npx ts-node -T client/dex.ts
