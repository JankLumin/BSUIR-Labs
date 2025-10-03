# настройка окружения

solana config set --url localhost
solana config set --url https://api.devnet.solana.com
solana config set --keypair ~/.config/solana/id.json

# запуск валидатора

solana-test-validator --reset

# новый ключ для первого аккаунта

solana-keygen new --outfile first.json
solana address -k ./first.json
FIRST=<address>

# выдача баланса

solana balance first.json
solana airdrop 10 $FIRST
solana balance first.json

# новый ключ для второго аккаунта

solana-keygen new --outfile second.json
SECOND=<address>

# перевод 1 SOL второму

solana transfer "$SECOND" 1 \
 --allow-unfunded-recipient \
 --from ./first.json \
 --no-wait
solana confirm <SIGNATURE>

# проверить балансы

solana balance first.json
solana balance second.json

---

python sol_helpers.py
