use anchor_lang::prelude::*;
use anchor_lang::solana_program::system_instruction;
use anchor_spl::token::{self, Burn};

use crate::common::CustomError;

#[account]
pub struct BankState {
    pub admin: Pubkey,
    pub buy_price_lamports: u64,
    pub sell_price_lamports: u64,
    pub bump: u8,
}

pub fn init_bank(ctx: Context<crate::InitBank>) -> Result<()> {
    let bank_state = &mut ctx.accounts.bank_state;
    bank_state.admin = ctx.accounts.admin.key();

    bank_state.buy_price_lamports = 100_000_000;
    bank_state.sell_price_lamports = 90_000_000;

    bank_state.bump = ctx.bumps.bank_state;
    msg!(
        "🏦 Bank initialized. Admin={}, buy={}, sell={}",
        bank_state.admin,
        bank_state.buy_price_lamports,
        bank_state.sell_price_lamports
    );
    Ok(())
}

pub fn update_prices(
    ctx: Context<crate::UpdatePrices>,
    buy_price_lamports: u64,
    sell_price_lamports: u64,
) -> Result<()> {
    require!(
        buy_price_lamports >= sell_price_lamports,
        CustomError::InvalidPriceConfig
    );
    let st = &mut ctx.accounts.bank_state;
    st.buy_price_lamports = buy_price_lamports;
    st.sell_price_lamports = sell_price_lamports;
    msg!("🔧 Prices updated: buy={}, sell={}", buy_price_lamports, sell_price_lamports);
    Ok(())
}

// вывод прибыли
pub fn withdraw(ctx: Context<crate::Withdraw>, amount: u64) -> Result<()> {
    let bank_wallet = &ctx.accounts.bank_wallet;
    let to = &ctx.accounts.to;

    let ix = system_instruction::transfer(&bank_wallet.key(), &to.key(), amount);
    let signer_seeds: &[&[&[u8]]] = &[&[b"bank", &[ctx.bumps.bank_wallet]]];

    anchor_lang::solana_program::program::invoke_signed(
        &ix,
        &[
            bank_wallet.to_account_info(),
            to.to_account_info(),
            ctx.accounts.system_program.to_account_info(),
        ],
        signer_seeds,
    )?;

    msg!("💸 Withdrawn {} lamports to {}", amount, to.key());
    Ok(())
}

pub fn sell_card(ctx: Context<crate::SellCard>) -> Result<()> {
    let user = &ctx.accounts.user;
    let bank_wallet = &ctx.accounts.bank_wallet;
    let mint = &ctx.accounts.mint;
    let token_account = &ctx.accounts.token_account;
    let card_meta = &ctx.accounts.card_meta;
    let state = &ctx.accounts.bank_state;

    require_keys_eq!(card_meta.mint_pubkey, mint.key(), CustomError::InvalidNFT);
    require_keys_eq!(token_account.owner, user.key(), CustomError::InvalidTokenOwner);
    require_keys_eq!(token_account.mint, mint.key(), CustomError::InvalidTokenMint);
    require!(token_account.amount == 1, CustomError::InvalidTokenAmount);

    let needed = state.sell_price_lamports;
    require!(
        bank_wallet.to_account_info().lamports() >= needed,
        CustomError::InsufficientBankLiquidity
    );

    let burn_accounts = Burn {
        mint: mint.to_account_info(),
        from: token_account.to_account_info(),
        authority: user.to_account_info(),
    };
    let cpi_ctx = CpiContext::new(ctx.accounts.token_program.to_account_info(), burn_accounts);
    token::burn(cpi_ctx, 1)?;

    let ix = system_instruction::transfer(&bank_wallet.key(), &user.key(), needed);
    let signer_seeds: &[&[&[u8]]] = &[&[b"bank", &[ctx.bumps.bank_wallet]]];

    anchor_lang::solana_program::program::invoke_signed(
        &ix,
        &[
            bank_wallet.to_account_info(),
            user.to_account_info(),
            ctx.accounts.system_program.to_account_info(),
        ],
        signer_seeds,
    )?;

    msg!(
        "💰 User {} sold NFT {} and received {} lamports",
        user.key(),
        mint.key(),
        needed
    );
    Ok(())
}
