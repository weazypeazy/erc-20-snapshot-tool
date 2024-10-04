from web3 import Web3
import pandas as pd

# Connect to Ethereum node (Infura as an example replace with your own rpc url if needed)
infura_url = "https://eth.llamarpc.com"
web3 = Web3(Web3.HTTPProvider(infura_url))

# Check if connection is successful
if web3.is_connected():
    print("Connected to Ethereum network")

# ERC-20 token contract address (replace with the address of your token)
contract_address = web3.to_checksum_address("<ERC20_CONTRACT_ADDRESS>")

# ABI of the contract (ERC-20 ABI, replace with the correct ABI if necessary)
abi = [
    {
        "constant": True,
        "inputs": [],
        "name": "name",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [
            {
                "name": "",
                "type": "uint8"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [
            {
                "name": "_owner",
                "type": "address"
            }
        ],
        "name": "balanceOf",
        "outputs": [
            {
                "name": "balance",
                "type": "uint256"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "constant": True,
        "inputs": [],
        "name": "symbol",
        "outputs": [
            {
                "name": "",
                "type": "string"
            }
        ],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "name": "from",
                "type": "address"
            },
            {
                "indexed": True,
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "name": "value",
                "type": "uint256"
            }
        ],
        "name": "Transfer",
        "type": "event"
    }
]

# Create the contract object
contract = web3.eth.contract(address=contract_address, abi=abi)

# Specify block range and batch size
start_block = 10569013  # Replace with your starting block
block_height = 20627000  # Replace with your desired snapshot block
initial_batch_size = 10000  # Adjust batch size if necessary

# Dictionary to hold balances
balances = {}

# Function to process logs
def process_logs(logs):
    for log in logs:
        event = contract.events.Transfer().process_log(log)
        from_address = event['args']['from']
        to_address = event['args']['to']
        value = event['args']['value']
        
        if from_address != '0x0000000000000000000000000000000000000000':  # Exclude minting events
            balances[from_address] = balances.get(from_address, 0) - value
        
        balances[to_address] = balances.get(to_address, 0) + value

# Function to fetch logs in batches
def fetch_logs_in_batches(from_block, to_block, batch_size):
    while from_block <= to_block:
        try:
            print(f"Fetching logs from block {from_block} to {min(from_block + batch_size - 1, to_block)}")
            logs = web3.eth.get_logs({
                'fromBlock': from_block,
                'toBlock': min(from_block + batch_size - 1, to_block),
                'address': contract_address,
                'topics': [web3.keccak(text="Transfer(address,address,uint256)").hex()]
            })
            process_logs(logs)
            from_block += batch_size
        except Exception as e:
            if "query exceeds max results" in str(e):
                print(f"Reducing batch size due to too many logs from blocks {from_block} to {from_block + batch_size - 1}")
                return fetch_logs_in_batches(from_block, to_block, batch_size // 2)
            else:
                print(f"Error fetching logs for blocks {from_block} to {min(from_block + batch_size - 1, to_block)}: {e}")
                break

# Start fetching logs
fetch_logs_in_batches(start_block, block_height, initial_batch_size)

# Export to CSV
df = pd.DataFrame(list(balances.items()), columns=['Address', 'Balance'])
df.to_csv(f'erc20_snapshot_block_{block_height}.csv', index=False)

print(f"Snapshot completed and saved to erc20_snapshot_block_{block_height}.csv")
