# Deposits and withdrawals

## Before depositing

Use the network, supported token contract and system destination supplied by the current environment. Identical token names do not mean identical contracts. Do not infer an address from this guide or reuse one from another deployment.

Deposits credit supported on-chain transfers. Send only assets that are supported and registered. Test with a small amount and verify the account credit before sending more. A transaction being broadcast or confirmed on-chain is different from the trading account being credited: the system must identify it and wait for the required confirmations.

On-chain token precision may exceed trading-ledger precision. Extra trailing precision is not credited. Allow for precision and network fees when comparing amounts.

## Withdrawing

A withdrawal requires wallet authorization. The trading account is debited before the on-chain payout, so there can be a delay between the debit and receipt. API wallets cannot withdraw.

Withdrawable funds differ from total balance. Unrealized profit or loss, initial margin, perpetual resting-order reserves, spot reservations and risk limits can all affect availability. Negative equity or a system withdrawal freeze may block withdrawals and transfers out.

Before submitting, verify the network, asset, amount and recipient information, and prepare any network fees needed by your wallet. After submitting, check withdrawal records and the on-chain transaction. A pending payout is not necessarily a failure; do not submit another identical withdrawal just because funds have not arrived.

## Account transfers and vaults

An account transfer changes ownership of assets within trading accounts; it is not an on-chain withdrawal. Positions and orders in the receiving account do not move with the funds. Transfers out are also subject to available funds and risk limits.

Use [Vault deposits](vaults.md) to invest in a vault. After redeeming shares, a separate withdrawal is needed to move funds on-chain.

## If funds have not arrived

Keep the network, token contract, transaction hash, amount, time and target account. Verify transaction success and asset support, then check deposit or withdrawal records. Never provide recovery phrases, private keys or API keys to anyone. Recovery of assets already sent on-chain depends on the circumstances and is not guaranteed.
