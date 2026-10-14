# Margin and funding

## Balance is not available margin

Account equity includes the margin-asset balance, unrealized profit or loss at the mark price, and accrued funding. Initial margin determines whether you can increase risk; maintenance margin determines liquidation eligibility. Spot reservations and perpetual resting-order margin reduce available funds.

Cross-margin positions in one account share collateral: losses in one market affect others. For isolated trading, verify the subaccount and margin mode. Platform markets use USDC margin; other trading venues may use different margin assets. Risk across different collateral currencies does not directly offset.

## Leverage

Higher leverage exposes the same equity to larger price-movement risk. Changing leverage changes margin requirements, not position size. A setting must be submitted and take effect; a page estimate is not the final account state. Reducing leverage requires more margin and can be rejected if funds are insufficient.

## Mark price and liquidation

Last trade, oracle and mark prices serve different purposes. Unrealized profit or loss and liquidation primarily use the mark price. Do not judge account safety from the last trade alone.

An account may be liquidated when equity cannot cover maintenance margin. Liquidation may cancel orders, close positions and incur liquidation fees; execution prices and losses depend on market conditions. Estimated liquidation prices change with funding, balances, positions and other markets. They are not fixed stop-loss levels. Insurance funds and auto-deleveraging do not guarantee principal or returns.

## Funding

Funding helps influence the difference between perpetual prices and the spot reference. At a positive rate, longs generally pay shorts; a negative rate reverses the direction. Without a perpetual position, you do not incur its funding payments.

Rates use an eight-hour basis; this does not mean settlement happens only every eight hours. The default calculation interval is one hour, prorated by interval length; consult the market configuration. For example, an eight-hour rate of 0.08% on a reference notional of 1,000 USDC for one hour, with unchanged prices and rates, corresponds to approximately 0.10 USDC. Actual amounts depend on the index, precision and time held.

Evaluate position performance using price profit or loss, trading fees and funding together. Check account risk and funding history, and keep available margin for changes.
