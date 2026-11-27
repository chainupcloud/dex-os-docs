# Escape guide

If a custody chain receives no new checkpoint root for a long time, anyone can use the open-source `dex-escape` tool to claim funds from the custody contracts back to their own wallet, without relying on this platform.

**Freezing is final**: a frozen custody chain never resumes operation. Each chain freezes on its own, and you claim each chain's assets on that chain.

## How an escape happens

- An escape goes: fresh coverage does not advance for 3 days → anyone requests → a 7-day wait (governance can extend it to 30 days) → the chain freezes on the latest root accepted at the deadline.
- Roots are still accepted during the wait.
- The deadline is anchored to that chain's latest fresh root and is at least 1 day after the request; a fresh root accepted while the request is pending cancels it.
- Requests, deadlines and freezes are per chain: a frozen chain stops only its own deposits and withdrawals and the cross-chain markets that involve it; other chains carry on.
- So as long as the latest root is pushed to every chain before its deadline, all chains freeze on the same root and both legs of a cross-chain trade stand or fall together.

Each chain's current mode and deadline are shown in the deposit and withdrawal status of the trading app: a chain with a pending escape request or a freeze is flagged and links to the in-app escape page.

## Claim with dex-escape

> Run `sync` before claiming: it pushes the latest signed root from the operators' signers to every chain (after the open-submission delay anyone can submit, paying only gas), so that every chain freezes on the same root.

1. **Prepare `chains.json`**: one entry per custody chain, keyed by custody key hash, with your own RPC for that chain.

   ```json
   {
     "<custody key hash>": { "rpc_url": "<RPC URL for that chain>" }
   }
   ```

2. **Check chain status**: each chain's mode, latest accepted root and deadline; it warns prominently when deadlines differ or a chain has no request.

   ```bash
   dex-escape status --chains chains.json
   ```

3. **Sync the final root**: fetch the latest signed package from an operator signer's read-only endpoint and push it to every chain that lags. Running it again does not repeat transactions. Signer and compute node read-only addresses are listed in the custody deployment file.

   ```bash
   dex-escape sync --chains chains.json --source <SIGNER_URL>[,<SIGNER_URL>…] --sender-key-file <GAS_KEY_FILE> --send true
   ```

   If a chain is stale (no fresh root for 3 days) and nobody has requested an escape yet, add `--request-escape true` to request it on all stale chains at once:

   ```bash
   dex-escape sync --chains chains.json --source <SIGNER_URL>[,<SIGNER_URL>…] --request-escape true --sender-key-file <GAS_KEY_FILE> --send true
   ```

4. **Claim per chain after the freeze**: each chain only pays the assets of its own custody group. The proof package, authorization and claim transaction are all bound to that chain.

   ```bash
   dex-escape prove --chain <custody key hash> --rpc <RPC_URL> --vault <custody vault address> --source <SIGNER_URL>[,<SIGNER_URL>…] --account <ACCOUNT_ID> --asset <ASSET_ID> --out escape-<chain>.json
   dex-escape authorize --package escape-<chain>.json --key-file <ACCOUNT_KEY_FILE>
   dex-escape claim --package escape-<chain>.json --rpc <RPC_URL> --sender-key-file <GAS_KEY_FILE> --send true
   ```

5. **Refund rejected deposits**: deposits the ledger rejected and has not refunded yet are refunded after the freeze to the receipt's beneficiary, using the refund proofs in the frozen root (before the freeze the operator's relay refunds them). Anyone can send these, paying only gas. `--recipient` lists only the refunds to that address; without it, every pending refund of the chain is listed.

   ```bash
   dex-escape refund --chain <custody key hash> --rpc <RPC_URL> --vault <custody vault address> --source <SIGNER_URL>[,<SIGNER_URL>…] --recipient <REFUND_ADDRESS> --sender-key-file <GAS_KEY_FILE> --send true
   ```

The `dex-escape --help` output is authoritative for the command shapes; values in angle brackets are yours to fill in. Take the custody vault address and custody key hash from the current environment's custody deployment, never from another deployment.

## Residual risks

- **Accepted residual risk**: if a chain cannot include our transactions for a full ~10 days (halted while its timestamps keep advancing, or censored), it may freeze on an older root.
- **One chain cannot include our transactions for ~10 days**: that chain freezes on an old root X_old while the other chains carry on; cross-chain trades involving that chain's assets after X_old are "half-undone" (a transfer of wealth between counterparties; the vaults do not become insolvent). Note: when a chain halts completely, even the escape request cannot get in, so it catches up after recovery and does not freeze; the danger is "timestamps advance but our transactions do not get in".
- **All chains stale at once with different deadlines**: all chains go stale while the ledger keeps trading (typically two or more funds verifiers offline for a long time), and the chains have different deadlines (requested at different times, governance extended only some chains, or nobody requested on some chain). If roots resume between the earliest and latest deadlines, the early-deadline chains freeze at X while the late-deadline or unrequested chains have their requests cancelled by the new root and carry on; cross-chain trades after X are half-undone.
- **What this means for you**: if a chain cannot include our transactions for ~10 days, cross-chain trades involving that chain during that time may be "half-undone". If all chains go stale at once, the deadlines are aligned across chains; as long as someone requests on every stale chain (`sync --request-escape`), all chains freeze on the same root.
