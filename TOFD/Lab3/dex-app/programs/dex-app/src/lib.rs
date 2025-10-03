use anchor_lang::prelude::*;
use anchor_spl::{
    associated_token::AssociatedToken,
    token::{self, Mint, Token, TokenAccount, Transfer},
};

declare_id!("4GYzDWQkmvpGkv4YjamGVZh9UTRKo81uoTwaiyjzzJdY");

#[program]
pub mod dex_app {
    use super::*;

    pub fn initialize(
        ctx: Context<Initialize>,
        init_your_amount: u64,
        init_wsol_amount: u64,
    ) -> Result<()> {
        let pool = &mut ctx.accounts.pool;

        pool.bump = ctx.bumps.pool_authority;
        pool.your_mint = ctx.accounts.your_mint.key();
        pool.wsol_mint = ctx.accounts.wsol_mint.key();

        pool.rate_num = 1;
        pool.rate_den = 2;

        pool.your_decimals = ctx.accounts.your_mint.decimals;
        pool.wsol_decimals = ctx.accounts.wsol_mint.decimals;

        token::transfer(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.user_your_ata.to_account_info(),
                    to: ctx.accounts.pool_your_ata.to_account_info(),
                    authority: ctx.accounts.payer.to_account_info(),
                },
            ),
            init_your_amount,
        )?;
        token::transfer(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.user_wsol_ata.to_account_info(),
                    to: ctx.accounts.pool_wsol_ata.to_account_info(),
                    authority: ctx.accounts.payer.to_account_info(),
                },
            ),
            init_wsol_amount,
        )?;
        Ok(())
    }

    pub fn buy(ctx: Context<Swap>, amount_wsol_in: u64) -> Result<()> {
        let pool = &ctx.accounts.pool;

        let scale_y = pow10(pool.your_decimals)?;
        let scale_w = pow10(pool.wsol_decimals)?;
        let your_out_u128 = (amount_wsol_in as u128)
            .checked_mul(scale_y)
            .and_then(|x| x.checked_mul(pool.rate_den as u128))
            .and_then(|x| x.checked_div((pool.rate_num as u128).checked_mul(scale_w)?))
            .ok_or(ErrorCode::MathOverflow)?;
        let your_out = u64::try_from(your_out_u128).map_err(|_| ErrorCode::MathOverflow)?;

        token::transfer(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.user_wsol_ata.to_account_info(),
                    to: ctx.accounts.pool_wsol_ata.to_account_info(),
                    authority: ctx.accounts.user.to_account_info(),
                },
            ),
            amount_wsol_in,
        )?;

        let pool_key = ctx.accounts.pool.key();
        let seeds: &[&[u8]] = &[b"pool", pool_key.as_ref(), &[pool.bump]];
        let signer = &[&seeds[..]];
        token::transfer(
            CpiContext::new_with_signer(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.pool_your_ata.to_account_info(),
                    to: ctx.accounts.user_your_ata.to_account_info(),
                    authority: ctx.accounts.pool_authority.to_account_info(),
                },
                signer,
            ),
            your_out,
        )?;
        Ok(())
    }

    pub fn sell(ctx: Context<Swap>, amount_your_in: u64) -> Result<()> {
        let pool = &ctx.accounts.pool;

        let scale_y = pow10(pool.your_decimals)?;
        let scale_w = pow10(pool.wsol_decimals)?;
        let wsol_out_u128 = (amount_your_in as u128)
            .checked_mul(scale_w)
            .and_then(|x| x.checked_mul(pool.rate_num as u128))
            .and_then(|x| x.checked_div((pool.rate_den as u128).checked_mul(scale_y)?))
            .ok_or(ErrorCode::MathOverflow)?;
        let wsol_out = u64::try_from(wsol_out_u128).map_err(|_| ErrorCode::MathOverflow)?;

        token::transfer(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.user_your_ata.to_account_info(),
                    to: ctx.accounts.pool_your_ata.to_account_info(),
                    authority: ctx.accounts.user.to_account_info(),
                },
            ),
            amount_your_in,
        )?;

        let pool_key = ctx.accounts.pool.key();
        let seeds: &[&[u8]] = &[b"pool", pool_key.as_ref(), &[pool.bump]];
        let signer = &[&seeds[..]];
        token::transfer(
            CpiContext::new_with_signer(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.pool_wsol_ata.to_account_info(),
                    to: ctx.accounts.user_wsol_ata.to_account_info(),
                    authority: ctx.accounts.pool_authority.to_account_info(),
                },
                signer,
            ),
            wsol_out,
        )?;
        Ok(())
    }
}

fn pow10(dec: u8) -> Result<u128> {
    let d = dec as u32;
    10u128
        .checked_pow(d)
        .ok_or(ErrorCode::MathOverflow.into())
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = payer, space = 8 + DexPool::LEN)]
    pub pool: Account<'info, DexPool>,
    #[account(seeds = [b"pool", pool.key().as_ref()], bump)]
    pub pool_authority: UncheckedAccount<'info>,

    pub your_mint: Account<'info, Mint>,
    pub wsol_mint: Account<'info, Mint>,

    #[account(init, payer = payer, associated_token::mint = your_mint, associated_token::authority = pool_authority)]
    pub pool_your_ata: Account<'info, TokenAccount>,
    #[account(init, payer = payer, associated_token::mint = wsol_mint, associated_token::authority = pool_authority)]
    pub pool_wsol_ata: Account<'info, TokenAccount>,

    #[account(mut)]
    pub user_your_ata: Account<'info, TokenAccount>,
    #[account(mut)]
    pub user_wsol_ata: Account<'info, TokenAccount>,

    #[account(mut)]
    pub payer: Signer<'info>,

    pub system_program: Program<'info, System>,
    pub token_program: Program<'info, Token>,
    pub associated_token_program: Program<'info, AssociatedToken>,
    pub rent: Sysvar<'info, Rent>,
}

#[derive(Accounts)]
pub struct Swap<'info> {
    #[account(mut)]
    pub pool: Account<'info, DexPool>,
    #[account(seeds = [b"pool", pool.key().as_ref()], bump = pool.bump)]
    pub pool_authority: UncheckedAccount<'info>,

    #[account(mut)]
    pub pool_your_ata: Account<'info, TokenAccount>,
    #[account(mut)]
    pub pool_wsol_ata: Account<'info, TokenAccount>,

    #[account(mut)]
    pub user_your_ata: Account<'info, TokenAccount>,
    #[account(mut)]
    pub user_wsol_ata: Account<'info, TokenAccount>,

    pub user: Signer<'info>,
    pub token_program: Program<'info, Token>,
}

#[account]
pub struct DexPool {
    pub bump: u8,
    pub your_mint: Pubkey,
    pub wsol_mint: Pubkey,
    pub rate_num: u64,
    pub rate_den: u64,
    pub your_decimals: u8,
    pub wsol_decimals: u8,
}
impl DexPool {
    pub const LEN: usize = 1 + 32 + 32 + 8 + 8 + 1 + 1;
}

#[error_code]
pub enum ErrorCode {
    #[msg("Math overflow")]
    MathOverflow,
}
