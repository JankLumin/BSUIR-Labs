use anchor_lang::prelude::*;
use anchor_spl::token::{self, Transfer};

use crate::common::CustomError;

pub const STATUS_OPEN: u8 = 0;
pub const STATUS_ACTIVE: u8 = 1;
pub const STATUS_FINISHED: u8 = 2;

#[account]
pub struct MatchAccount {
    pub match_id: u64,
    pub bump: u8,
    pub status: u8,
    pub creator: Pubkey,
    pub opponent: Pubkey,
    pub creator_mint: Pubkey,
    pub opponent_mint: Pubkey,
    pub creator_card_type: u8,
    pub opponent_card_type: u8,
    pub timestamp: i64,
}

impl MatchAccount {
    pub const SIZE: usize = 8
        + 1
        + 1
        + 32 + 32
        + 32 + 32
        + 1 + 1
        + 8;
}

pub fn create_match(ctx: Context<crate::CreateMatch>, match_id: u64) -> Result<()> {
    let creator = &ctx.accounts.creator;
    let match_acc = &mut ctx.accounts.match_account;
    let creator_mint = &ctx.accounts.creator_mint;
    let creator_token_account = &ctx.accounts.creator_token_account;
    let escrow_creator = &ctx.accounts.escrow_creator;
    let card_meta = &ctx.accounts.card_meta;

    require_keys_eq!(creator_token_account.owner, creator.key(), CustomError::InvalidTokenOwner);
    require_keys_eq!(creator_token_account.mint, creator_mint.key(), CustomError::InvalidTokenMint);
    require!(creator_token_account.amount == 1, CustomError::InvalidTokenAmount);

    require_keys_eq!(card_meta.mint_pubkey, creator_mint.key(), CustomError::InvalidNFT);

    let cpi = CpiContext::new(
        ctx.accounts.token_program.to_account_info(),
        Transfer {
            from: creator_token_account.to_account_info(),
            to: escrow_creator.to_account_info(),
            authority: creator.to_account_info(),
        },
    );
    token::transfer(cpi, 1)?;

    match_acc.match_id = match_id;
    match_acc.bump = ctx.bumps.match_account;
    match_acc.status = STATUS_OPEN;
    match_acc.creator = creator.key();
    match_acc.opponent = Pubkey::default();
    match_acc.creator_mint = creator_mint.key();
    match_acc.opponent_mint = Pubkey::default();
    match_acc.creator_card_type = card_meta.card_type;
    match_acc.opponent_card_type = u8::MAX;
    match_acc.timestamp = Clock::get()?.unix_timestamp;

    msg!("🆕 Match {} created by {}", match_id, creator.key());
    Ok(())
}

pub fn join_match(ctx: Context<crate::JoinMatch>, _match_id: u64) -> Result<()> {
    let opponent = &ctx.accounts.opponent;
    let match_acc = &mut ctx.accounts.match_account;
    let opponent_mint = &ctx.accounts.opponent_mint;
    let opponent_token_account = &ctx.accounts.opponent_token_account;
    let escrow_opponent = &ctx.accounts.escrow_opponent;
    let card_meta = &ctx.accounts.card_meta_opponent;

    require!(match_acc.status == STATUS_OPEN, CustomError::MatchNotOpen);
    require!(match_acc.creator != opponent.key(), CustomError::SamePlayer);

    require_keys_eq!(opponent_token_account.owner, opponent.key(), CustomError::InvalidTokenOwner);
    require_keys_eq!(opponent_token_account.mint, opponent_mint.key(), CustomError::InvalidTokenMint);
    require!(opponent_token_account.amount == 1, CustomError::InvalidTokenAmount);

    require_keys_eq!(card_meta.mint_pubkey, opponent_mint.key(), CustomError::InvalidNFT);

    let cpi = CpiContext::new(
        ctx.accounts.token_program.to_account_info(),
        Transfer {
            from: opponent_token_account.to_account_info(),
            to: escrow_opponent.to_account_info(),
            authority: opponent.to_account_info(),
        },
    );
    token::transfer(cpi, 1)?;

    match_acc.opponent = opponent.key();
    match_acc.opponent_mint = opponent_mint.key();
    match_acc.opponent_card_type = card_meta.card_type;
    match_acc.status = STATUS_ACTIVE;

    msg!("🤝 Match {} joined by {}", match_acc.match_id, opponent.key());
    Ok(())
}

pub fn resolve_match(ctx: Context<crate::ResolveMatch>, _match_id: u64) -> Result<()> {
    let resolver = &ctx.accounts.resolver;
    let m = &mut ctx.accounts.match_account;

    require!(resolver.key() == m.creator || resolver.key() == m.opponent, CustomError::NotParticipant);
    require!(m.status == STATUS_ACTIVE, CustomError::MatchNotActive);

    require_keys_eq!(ctx.accounts.escrow_creator.owner, m.key(), CustomError::InvalidEscrow);
    require_keys_eq!(ctx.accounts.escrow_creator.mint, m.creator_mint, CustomError::InvalidEscrow);
    require!(ctx.accounts.escrow_creator.amount == 1, CustomError::InvalidTokenAmount);

    require_keys_eq!(ctx.accounts.escrow_opponent.owner, m.key(), CustomError::InvalidEscrow);
    require_keys_eq!(ctx.accounts.escrow_opponent.mint, m.opponent_mint, CustomError::InvalidEscrow);
    require!(ctx.accounts.escrow_opponent.amount == 1, CustomError::InvalidTokenAmount);

    require_keys_eq!(ctx.accounts.creator_dst_creator_mint.owner, m.creator, CustomError::InvalidTokenOwner);
    require_keys_eq!(ctx.accounts.creator_dst_creator_mint.mint, m.creator_mint, CustomError::InvalidTokenMint);

    require_keys_eq!(ctx.accounts.creator_dst_opponent_mint.owner, m.creator, CustomError::InvalidTokenOwner);
    require_keys_eq!(ctx.accounts.creator_dst_opponent_mint.mint, m.opponent_mint, CustomError::InvalidTokenMint);

    require_keys_eq!(ctx.accounts.opponent_dst_creator_mint.owner, m.opponent, CustomError::InvalidTokenOwner);
    require_keys_eq!(ctx.accounts.opponent_dst_creator_mint.mint, m.creator_mint, CustomError::InvalidTokenMint);

    require_keys_eq!(ctx.accounts.opponent_dst_opponent_mint.owner, m.opponent, CustomError::InvalidTokenOwner);
    require_keys_eq!(ctx.accounts.opponent_dst_opponent_mint.mint, m.opponent_mint, CustomError::InvalidTokenMint);

    let a = m.creator_card_type;
    let b = m.opponent_card_type;
    let outcome = ((a as i16 - b as i16 + 3) % 3) as u8;

    let match_id_le = m.match_id.to_le_bytes();
    let signer_seeds: &[&[&[u8]]] = &[&[b"match", match_id_le.as_ref(), &[m.bump]]];

    use anchor_spl::token::Transfer as SplTransfer;
    let tp = ctx.accounts.token_program.to_account_info();

    match outcome {
        0 => {
            let cpi1 = CpiContext::new_with_signer(
                tp.clone(),
                SplTransfer {
                    from: ctx.accounts.escrow_creator.to_account_info(),
                    to: ctx.accounts.creator_dst_creator_mint.to_account_info(),
                    authority: m.to_account_info(),
                },
                signer_seeds,
            );
            token::transfer(cpi1, 1)?;

            let cpi2 = CpiContext::new_with_signer(
                tp.clone(),
                SplTransfer {
                    from: ctx.accounts.escrow_opponent.to_account_info(),
                    to: ctx.accounts.opponent_dst_opponent_mint.to_account_info(),
                    authority: m.to_account_info(),
                },
                signer_seeds,
            );
            token::transfer(cpi2, 1)?;
        }
        1 => {
            let cpi1 = CpiContext::new_with_signer(
                tp.clone(),
                SplTransfer {
                    from: ctx.accounts.escrow_creator.to_account_info(),
                    to: ctx.accounts.creator_dst_creator_mint.to_account_info(),
                    authority: m.to_account_info(),
                },
                signer_seeds,
            );
            token::transfer(cpi1, 1)?;

            let cpi2 = CpiContext::new_with_signer(
                tp.clone(),
                SplTransfer {
                    from: ctx.accounts.escrow_opponent.to_account_info(),
                    to: ctx.accounts.creator_dst_opponent_mint.to_account_info(),
                    authority: m.to_account_info(),
                },
                signer_seeds,
            );
            token::transfer(cpi2, 1)?;
        }
        _ => {
            let cpi1 = CpiContext::new_with_signer(
                tp.clone(),
                SplTransfer {
                    from: ctx.accounts.escrow_creator.to_account_info(),
                    to: ctx.accounts.opponent_dst_creator_mint.to_account_info(),
                    authority: m.to_account_info(),
                },
                signer_seeds,
            );
            token::transfer(cpi1, 1)?;

            let cpi2 = CpiContext::new_with_signer(
                tp.clone(),
                SplTransfer {
                    from: ctx.accounts.escrow_opponent.to_account_info(),
                    to: ctx.accounts.opponent_dst_opponent_mint.to_account_info(),
                    authority: m.to_account_info(),
                },
                signer_seeds,
            );
            token::transfer(cpi2, 1)?;
        }
    }

    m.status = STATUS_FINISHED;
    m.timestamp = Clock::get()?.unix_timestamp;
    msg!("🏁 Match {} resolved: outcome {}", m.match_id, outcome);
    Ok(())
}
