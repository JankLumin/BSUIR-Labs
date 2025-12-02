use anchor_lang::prelude::*;
use anchor_lang::solana_program::{program::invoke, sysvar, system_instruction};
use anchor_spl::token::{self, MintTo, SetAuthority};
use anchor_spl::token::spl_token::instruction::AuthorityType;

use mpl_token_metadata::instructions::{
    CreateMetadataAccountV3, CreateMetadataAccountV3InstructionArgs,
    CreateMasterEditionV3, CreateMasterEditionV3InstructionArgs,
};
use mpl_token_metadata::types::DataV2;

use crate::MintCard;

#[account]
pub struct CardMeta {
    pub owner: Pubkey,
    pub mint_pubkey: Pubkey,
    pub card_type: u8,
    pub mint_time: i64,
    pub bump: u8,
}

pub fn mint_card(
    ctx: Context<MintCard>,
    card_type: u8,
    name: String,
    symbol: String,
    uri: String,
) -> Result<()> {
    let user = &ctx.accounts.user;
    let mint = &ctx.accounts.mint;

    // 1. Оплата банку
    let price = ctx.accounts.bank_state.buy_price_lamports;
    let ix_pay = system_instruction::transfer(&user.key(), &ctx.accounts.bank_wallet.key(), price);
    anchor_lang::solana_program::program::invoke(
        &ix_pay,
        &[
            user.to_account_info(),
            ctx.accounts.bank_wallet.to_account_info(),
            ctx.accounts.system_program.to_account_info(),
        ],
    )?;

    // 2. Минт токена (NFT)
    let cpi_accounts = MintTo {
        mint: mint.to_account_info(),
        to: ctx.accounts.token_account.to_account_info(),
        authority: user.to_account_info(),
    };
    let cpi_ctx = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
    token::mint_to(cpi_ctx, 1)?;

    // 3. Создание аккаунта Metadata
    let data_v2 = DataV2 {
        name,
        symbol,
        uri,
        seller_fee_basis_points: 0,
        creators: None,
        collection: None,
        uses: None,
    };
    let metadata_args = CreateMetadataAccountV3InstructionArgs {
        data: data_v2,
        is_mutable: true,
        collection_details: None,
    };
    let metadata_ix = CreateMetadataAccountV3 {
        metadata: ctx.accounts.metadata.key(),
        mint: mint.key(),
        mint_authority: user.key(),
        payer: user.key(),
        update_authority: (user.key(), true),
        system_program: ctx.accounts.system_program.key(),
        rent: Some(sysvar::rent::ID),
    }
    .instruction(metadata_args);

    invoke(
        &metadata_ix,
        &[
            // Это аккаунты, которые требует инструкция CreateMetadataAccountV3
            ctx.accounts.metadata.to_account_info(),
            mint.to_account_info(),
            user.to_account_info(), // mint_authority
            user.to_account_info(), // payer
            user.to_account_info(), // update_authority
            ctx.accounts.system_program.to_account_info(),
            ctx.accounts.rent.to_account_info(),
            // И сама программа Metaplex
            ctx.accounts.token_metadata_program.to_account_info(),
            ctx.accounts.sysvar_instructions.to_account_info(),
        ],
    )?;

    // 4. Создание аккаунта Master Edition 
    let me_args = CreateMasterEditionV3InstructionArgs { max_supply: Some(0) }; // 0 = Non-Fungible
    let me_ix = CreateMasterEditionV3 {
        edition: ctx.accounts.master_edition.key(),
        mint: mint.key(),
        update_authority: user.key(),
        mint_authority: user.key(),
        payer: user.key(),
        metadata: ctx.accounts.metadata.key(),
        token_program: ctx.accounts.token_program.key(),
        system_program: ctx.accounts.system_program.key(),
        rent: Some(sysvar::rent::ID),
    }
    .instruction(me_args);

    invoke(
        &me_ix,
        &[
            // Аккаунты для CreateMasterEditionV3
            ctx.accounts.master_edition.to_account_info(),
            mint.to_account_info(),
            ctx.accounts.token_account.to_account_info(),
            user.to_account_info(), // update_authority
            user.to_account_info(), // mint_authority
            user.to_account_info(), // payer
            ctx.accounts.metadata.to_account_info(),
            ctx.accounts.token_program.to_account_info(),
            ctx.accounts.system_program.to_account_info(),
            ctx.accounts.rent.to_account_info(),
            // И сама программа Metaplex
            ctx.accounts.token_metadata_program.to_account_info(),
            ctx.accounts.sysvar_instructions.to_account_info(),
        ],
    )?;

    // 5. Запись кастомных данных (CardMeta)
    let clock = Clock::get()?;
    let card_meta = &mut ctx.accounts.card_meta;
    card_meta.owner = user.key();
    card_meta.mint_pubkey = mint.key();
    card_meta.card_type = card_type;
    card_meta.mint_time = clock.unix_timestamp;
    card_meta.bump = ctx.bumps.card_meta;

    // {
    //     let cpi_accounts = SetAuthority {
    //         account_or_mint: ctx.accounts.mint.to_account_info(),
    //         current_authority: user.to_account_info(),
    //     };
    //     let cpi_ctx = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
    //     token::set_authority(cpi_ctx, AuthorityType::MintTokens, None)?;
    // }
    // {
    //     let cpi_accounts = SetAuthority {
    //         account_or_mint: ctx.accounts.mint.to_account_info(),
    //         current_authority: user.to_account_info(),
    //     };
    //     let cpi_ctx = CpiContext::new(ctx.accounts.token_program.to_account_info(), cpi_accounts);
    //     token::set_authority(cpi_ctx, AuthorityType::FreezeAccount, None)?;
    // }

    msg!("✅ Minted NFT {:?}", mint.key());
    Ok(())
}