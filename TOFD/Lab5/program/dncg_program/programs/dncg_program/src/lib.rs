use anchor_lang::prelude::*;
use anchor_lang::system_program;
use anchor_spl::associated_token::AssociatedToken;
use anchor_spl::token::{Token, Mint, TokenAccount};
use mpl_token_metadata::ID as token_metadata_id;

pub mod mint;
pub mod game_match;
pub mod common;
pub mod bank;

declare_id!("Bo5ZQnDamED9cePN5VKAa8ZSPrtjahYgzD5UQtSFYsmr");

#[derive(Accounts)]
#[instruction(card_type: u8)]
pub struct MintCard<'info> {
    #[account(mut)]
    pub user: Signer<'info>,

    #[account(
        init,
        payer = user,
        mint::decimals = 0,
        mint::authority = user,
        mint::freeze_authority = user
    )]
    pub mint: Account<'info, Mint>,

    #[account(
        init,
        payer = user,
        associated_token::mint = mint,
        associated_token::authority = user
    )]
    pub token_account: Account<'info, TokenAccount>,

    /// CHECK: Metaplex metadata PDA (owned by token-metadata program)
    // #[account(
    //     init,
    //     payer = user,
    //     space = 8 + 300,
    //     seeds = [
    //         b"metadata",
    //         token_metadata_id.to_bytes().as_ref(),
    //         mint.key().as_ref()
    //     ],
    //     bump,
    //     owner = token_metadata_id
    // )]
    #[account(mut)]
    pub metadata: UncheckedAccount<'info>,

    /// CHECK: Master Edition PDA (owned by token-metadata program)
    // #[account(
    //     init,
    //     payer = user,
    //     space = 8 + 282,
    //     seeds = [
    //         b"metadata",
    //         token_metadata_id.to_bytes().as_ref(),
    //         mint.key().as_ref(),
    //         b"edition"
    //     ],
    //     bump,
    //     owner = token_metadata_id
    // )]
    #[account(mut)]
    pub master_edition: UncheckedAccount<'info>,

    #[account(
        init,
        payer = user,
        space = 8 + 32 + 32 + 1 + 8 + 1,
        seeds = [b"card", mint.key().as_ref()],
        bump
    )]
    pub card_meta: Account<'info, crate::mint::CardMeta>,

    /// CHECK: Bank wallet PDA
    #[account(mut, seeds = [b"bank"], bump, owner = system_program::ID)]
    pub bank_wallet: UncheckedAccount<'info>,

    #[account(seeds = [b"bank_state"], bump)]
    pub bank_state: Account<'info, crate::bank::BankState>,

    pub token_program: Program<'info, Token>,
    pub associated_token_program: Program<'info, AssociatedToken>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,

    /// CHECK: Metaplex Token Metadata Program
    #[account(address = token_metadata_id)]
    pub token_metadata_program: UncheckedAccount<'info>,

    /// CHECK: Instructions sysvar (required by some mpl instructions)
    #[account(address = anchor_lang::solana_program::sysvar::instructions::ID)]
    pub sysvar_instructions: UncheckedAccount<'info>,
}

#[derive(Accounts)]
#[instruction(match_id: u64)]
pub struct CreateMatch<'info> {
    #[account(mut)]
    pub creator: Signer<'info>,
    #[account(init, payer = creator, space = 8 + crate::game_match::MatchAccount::SIZE, seeds = [b"match", match_id.to_le_bytes().as_ref()], bump)]
    pub match_account: Account<'info, crate::game_match::MatchAccount>,
    #[account(mut)]
    pub creator_mint: Account<'info, Mint>,
    #[account(mut, associated_token::mint = creator_mint, associated_token::authority = creator)]
    pub creator_token_account: Account<'info, TokenAccount>,
    #[account(seeds = [b"card", creator_mint.key().as_ref()], bump = card_meta.bump)]
    pub card_meta: Account<'info, crate::mint::CardMeta>,
    #[account(init, payer = creator, associated_token::mint = creator_mint, associated_token::authority = match_account)]
    pub escrow_creator: Account<'info, TokenAccount>,
    pub token_program: Program<'info, Token>,
    pub associated_token_program: Program<'info, AssociatedToken>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
#[instruction(match_id: u64)]
pub struct JoinMatch<'info> {
    #[account(mut)]
    pub opponent: Signer<'info>,
    #[account(mut, seeds = [b"match", match_id.to_le_bytes().as_ref()], bump = match_account.bump)]
    pub match_account: Account<'info, crate::game_match::MatchAccount>,
    #[account(mut)]
    pub opponent_mint: Account<'info, Mint>,
    #[account(mut, associated_token::mint = opponent_mint, associated_token::authority = opponent)]
    pub opponent_token_account: Account<'info, TokenAccount>,
    #[account(seeds = [b"card", opponent_mint.key().as_ref()], bump = card_meta_opponent.bump)]
    pub card_meta_opponent: Account<'info, crate::mint::CardMeta>,
    #[account(init, payer = opponent, associated_token::mint = opponent_mint, associated_token::authority = match_account)]
    pub escrow_opponent: Account<'info, TokenAccount>,
    pub token_program: Program<'info, Token>,
    pub associated_token_program: Program<'info, AssociatedToken>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
#[instruction(match_id: u64)]
pub struct ResolveMatch<'info> {
    #[account(mut)]
    pub resolver: Signer<'info>,

    #[account(
        mut,
        seeds = [b"match", match_id.to_le_bytes().as_ref()],
        bump = match_account.bump
    )]
    pub match_account: Account<'info, crate::game_match::MatchAccount>,

    pub creator: AccountInfo<'info>,

    pub opponent: AccountInfo<'info>,

    pub creator_mint: Account<'info, Mint>,
    pub opponent_mint: Account<'info, Mint>,


    // Escrow аккаунты
    #[account(
        mut,
        associated_token::mint = creator_mint,
        associated_token::authority = match_account
    )]
    pub escrow_creator: Account<'info, TokenAccount>,

    #[account(
        mut,
        associated_token::mint = opponent_mint,
        associated_token::authority = match_account
    )]
    pub escrow_opponent: Account<'info, TokenAccount>,

    #[account(
        init_if_needed,
        payer = resolver,
        associated_token::mint = creator_mint,
        associated_token::authority = creator
    )]
    pub creator_dst_creator_mint: Account<'info, TokenAccount>,

    #[account(
        init_if_needed,
        payer = resolver,
        associated_token::mint = opponent_mint,
        associated_token::authority = creator
    )]
    pub creator_dst_opponent_mint: Account<'info, TokenAccount>,

    #[account(
        init_if_needed,
        payer = resolver,
        associated_token::mint = creator_mint,
        associated_token::authority = opponent
    )]
    pub opponent_dst_creator_mint: Account<'info, TokenAccount>,

    #[account(
        init_if_needed,
        payer = resolver,
        associated_token::mint = opponent_mint,
        associated_token::authority = opponent
    )]
    pub opponent_dst_opponent_mint: Account<'info, TokenAccount>,

    pub token_program: Program<'info, Token>,
    pub associated_token_program: Program<'info, AssociatedToken>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct InitBank<'info> {
    #[account(mut)]
    pub admin: Signer<'info>,
    #[account(init, payer = admin, space = 8 + 32 + 8 + 8 + 1, seeds = [b"bank_state"], bump)]
    pub bank_state: Account<'info, crate::bank::BankState>,

    #[account(init, payer = admin, space = 0, seeds = [b"bank"], bump, owner = system_program::ID)]
    pub bank_wallet: UncheckedAccount<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct SellCard<'info> {
    #[account(mut)]
    pub user: Signer<'info>,

    #[account(mut, seeds = [b"bank"], bump, owner = system_program::ID)]
    pub bank_wallet: UncheckedAccount<'info>,
    #[account(mut, seeds = [b"bank_state"], bump)]
    pub bank_state: Account<'info, crate::bank::BankState>,
    #[account(mut, seeds = [b"card", mint.key().as_ref()], bump = card_meta.bump, close = user)]
    pub card_meta: Account<'info, crate::mint::CardMeta>,
    #[account(mut)]
    pub mint: Account<'info, Mint>,
    #[account(mut, associated_token::mint = mint, associated_token::authority = user)]
    pub token_account: Account<'info, TokenAccount>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct UpdatePrices<'info> {
    pub admin: Signer<'info>,
    #[account(mut, seeds = [b"bank_state"], bump, has_one = admin)]
    pub bank_state: Account<'info, crate::bank::BankState>,
}

#[derive(Accounts)]
pub struct Withdraw<'info> {
    pub admin: Signer<'info>,
    #[account(mut, seeds = [b"bank_state"], bump, has_one = admin)]
    pub bank_state: Account<'info, crate::bank::BankState>,
    
    #[account(mut, seeds = [b"bank"], bump, owner = system_program::ID)]
    pub bank_wallet: UncheckedAccount<'info>,
    
    #[account(mut, owner = system_program::ID)]
    pub to: UncheckedAccount<'info>,
    pub system_program: Program<'info, System>,
}

#[program]
pub mod dncg_program {
    use super::*;

    pub fn mint_card(ctx: Context<MintCard>, card_type: u8, name: String, symbol: String, uri: String) -> Result<()> {
        mint::mint_card(ctx, card_type, name, symbol, uri)
    }

    pub fn create_match(ctx: Context<CreateMatch>, match_id: u64) -> Result<()> {
        game_match::create_match(ctx, match_id)
    }
    pub fn join_match(ctx: Context<JoinMatch>, match_id: u64) -> Result<()> {
        game_match::join_match(ctx, match_id)
    }
    pub fn resolve_match(ctx: Context<ResolveMatch>, match_id: u64) -> Result<()> {
        game_match::resolve_match(ctx, match_id)
    }

    pub fn init_bank(ctx: Context<InitBank>) -> Result<()> { bank::init_bank(ctx) }
    pub fn sell_card(ctx: Context<SellCard>) -> Result<()> { bank::sell_card(ctx) }
    pub fn update_prices(ctx: Context<UpdatePrices>, buy_price_lamports: u64, sell_price_lamports: u64) -> Result<()> {
        bank::update_prices(ctx, buy_price_lamports, sell_price_lamports)
    }
    pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> { bank::withdraw(ctx, amount) }
}
