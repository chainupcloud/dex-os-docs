# Getting started

Unibook supports perpetual futures and spot trading. They share an account, but use assets differently: spot trades are fully funded; perpetuals require margin and can incur funding payments and liquidation.

## Your first trade

1. Verify the site's network, supported assets and markets. Testnet assets differ from real assets; never send funds across networks.
2. Connect a wallet you control and confirm the account you are operating. Main accounts, subaccounts and vault accounts have separate balances and risk.
3. Follow [Deposits and withdrawals](deposits-and-withdrawals.md) to verify the network, token contract and destination, then test with a small deposit.
4. Check price and size increments, fees and market status. For perpetuals, also check margin, leverage and funding.
5. Set the price, size and time in force, review the operation in your wallet and submit.
6. Check order status, fills and balances. Successful submission does not mean the entire order filled.

## Accounts and authorization

One wallet can own multiple accounts. Subaccounts let you manage funds and positions separately; perpetual positions within one account generally share margin. Moving funds to another account does not move existing orders or positions.

An API wallet is a trading key authorized by your main wallet. It can perform trading operations within its scope, but cannot withdraw or transfer funds. Authorizations have their own expiry; revoke them when no longer needed. Never share your main wallet or API wallet private key.

## Next steps

Read [Orders and fills](trading.md), [Margin and funding](margin-and-funding.md), or [Vaults](vaults.md). Developer integrations must also follow API signing, precision and request limits.
