# ERC-20 Snapshot Tool

This Python tool allows you to take a snapshot of ERC-20 token balances at a specific block height by processing `Transfer` events. It fetches token transfer logs from the blockchain in batches and computes the final token balances for each address, exporting the results to a CSV file.

## Features

- Connects to an Ethereum node using `web3.py` (Infura or any other provider).
- Fetches `Transfer` logs in batches to avoid exceeding node limitations.
- Calculates the final balance of each address based on transfers up to the specified block height.
- Saves the snapshot of token balances in CSV format.

## Prerequisites

- Python 3.7 or higher.
- Install the required Python packages:
  ```bash
  pip install web3 pandas


1. **Edit the Script**:
   - Replace `<ERC20_CONTRACT_ADDRESS>` with the actual contract address of the ERC-20 token you want to snapshot.
   - Modify the `start_block` and `block_height` variables to match your snapshot requirements.

2. **Run the Script**:
   After making the necessary changes, run the script using Python:
   ```bash
   python snapshot_tool.py
