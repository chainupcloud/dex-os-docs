# Orders and fills

## Spot and perpetuals

A spot buy needs available quote assets; a sell needs available base assets. Resting orders reserve the required funds, which are released as the order is canceled, expires or fills. Spot fees are deducted from the asset received.

Perpetual orders change a contract position without delivering the underlying asset. Positions and resting orders can both use margin. Reduce-only orders decrease an existing position and cannot open a position in the opposite direction.

## Time in force

| Type | Behavior |
| --- | --- |
| GTC | Fill immediately where possible; rest the remainder until canceled or expired. |
| IOC | Fill immediately where possible and cancel the remainder. |
| FOK | Fill the entire order or cancel it. |
| Post-only | Rest on the book; reject if it would immediately take liquidity. |

A limit sets your worst acceptable price; it does not guarantee a fill. Orders match by price priority, then time priority, at the resting order's price. An order can fill partially across several prices. New orders do not trade against resting orders in the same account.

## Canceling and modifying

An order may fill before a cancellation arrives; check the final order and fill records. Modifying an order loses its original time priority. Batch operations may partially succeed: inspect each result rather than treating the batch as one transaction.

## Conditional orders, TP/SL and TWAP

Perpetual trading supports conditional orders, take-profit/stop-loss and TWAP. Conditional orders trigger on the mark price. Triggering does not guarantee execution: liquidity, limits, margin and market status still apply. TWAP splits a target size into scheduled slices. Unfilled slices are not guaranteed to be recovered, so total fills may be below the target.

## Fees and rejections

Trading fees depend on market rates, account tiers and order attribution. Some markets may also charge deployer or builder fees. Use current market information and fill details rather than applying one default rate to every market.

Misaligned prices or sizes, insufficient margin, paused markets and incorrect reduce-only directions can cause rejection. Check the specific error and correct the request before submitting again.
