use anchor_lang::prelude::*;

declare_id!("FuB4rAMim4zH8sffBdv8kBSgCVLUsmaphX72rrScuPSB");

#[program]
pub mod counter_app {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let acc = &mut ctx.accounts.counter;
        acc.value = 0;
        acc.authority = ctx.accounts.authority.key();
        Ok(())
    }

    pub fn increment(ctx: Context<Update>) -> Result<()> {
        let acc = &mut ctx.accounts.counter;
        require_keys_eq!(acc.authority, ctx.accounts.authority.key(), CounterError::Unauthorized);
        acc.value = acc.value.checked_add(1).ok_or(CounterError::Overflow)?;
        Ok(())
    }

    pub fn decrement(ctx: Context<Update>) -> Result<()> {
        let acc = &mut ctx.accounts.counter;
        require_keys_eq!(acc.authority, ctx.accounts.authority.key(), CounterError::Unauthorized);
        acc.value = acc.value.checked_sub(1).ok_or(CounterError::Underflow)?;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = authority, space = 8 + 8 + 32)]
    pub counter: Account<'info, CounterAcc>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Update<'info> {
    #[account(mut)]
    pub counter: Account<'info, CounterAcc>,
    pub authority: Signer<'info>,
}

#[account]
pub struct CounterAcc {
    pub value: u64,
    pub authority: Pubkey,
}

#[error_code]
pub enum CounterError {
    #[msg("Only authority may modify the counter")]
    Unauthorized,
    #[msg("Counter overflow")]
    Overflow,
    #[msg("Counter underflow")]
    Underflow,
}
