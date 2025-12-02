use anchor_lang::prelude::*;

#[error_code]
pub enum CustomError {
    #[msg("You are not the owner of this NFT")]
    NotOwner,
    #[msg("This NFT does not belong to the DNCG collection")]
    InvalidNFT,
    #[msg("Invalid mint authority")]
    InvalidMintAuthority,
    #[msg("Token account amount must be 1")]
    InvalidTokenAmount,
    #[msg("Token account owner mismatch")]
    InvalidTokenOwner,
    #[msg("Token account mint mismatch")]
    InvalidTokenMint,
    #[msg("Bank has not enough SOL")]
    InsufficientBankLiquidity,
    #[msg("Invalid price configuration")]
    InvalidPriceConfig,

    #[msg("Match is not open")]
    MatchNotOpen,
    #[msg("Match is not active")]
    MatchNotActive,
    #[msg("Match already resolved")]
    MatchAlreadyResolved,
    #[msg("You are not a participant of this match")]
    NotParticipant,
    #[msg("Same player cannot join their own match")]
    SamePlayer,
    #[msg("Escrow account is invalid")]
    InvalidEscrow,
}
