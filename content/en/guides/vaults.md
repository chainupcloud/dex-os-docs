# Vaults

A vault lets depositors contribute funds and receive shares while a manager trades within the vault's constraints. Share value changes with strategy performance. Historical returns and displayed annualized figures do not predict future returns.

## Before depositing

- Review the manager, strategy, allowed markets and leverage limits.
- Check profit sharing, minimum deposit and deposit cap.
- Check lock duration, redemption windows and minimum manager contribution.
- Review equity, share value, historical performance and available liquidity.

Deposits mint shares at the current value of the relevant share class. Depositors and managers use different share classes. Earlier profit or loss is accounted for before a deposit; do not assume a deposit buys a fixed number of shares.

## Profit, loss and fees

Profits are allocated under the vault rules. Performance sharing applies to eligible gains above the high-water mark, rather than charging again each time losses are recovered. The manager's share class receives that fee. Losses reduce share value. Share minting and redemption round down; very small operations may be rejected because the resulting shares or amount are too small.

## Redeeming

Redemption requires the lock to expire, the redemption window to be open, and sufficient available funds in the main vault account. A new deposit resets the lock on all shares that depositor holds in the vault, not only the new shares. Owning shares does not mean all corresponding assets are immediately withdrawable. Share value continues to change before redemption.

Do not transfer directly to a vault account to buy shares. Use the vault deposit flow. A regular asset deposit and a vault deposit are different operations.

## Manager constraints

Managers are subject to market allowlists, denylists and leverage limits. If a manager-contribution circuit breaker is configured, an insufficient manager ratio can halt trading, cancel orders and force positions closed. Trading can resume only once recovery conditions are met. These constraints limit the strategy; they do not guarantee profits or immediate redemption.
