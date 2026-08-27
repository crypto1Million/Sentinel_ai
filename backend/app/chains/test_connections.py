from dotenv import load_dotenv

load_dotenv()

from chains.evm import EVMChainClient
from chains.registry import CHAINS


def test_all_evm_chains():

    print("\n=== SentinelAI EVM Chain Connection Test ===\n")

    for config in CHAINS.values():

        if config.chain_type.value != "evm":
            continue

        print(f"Testing {config.name}...")

        try:
            client = EVMChainClient(config.id)

            block = client.latest_block()

            print(f"  ✓ {config.name}")
            print(f"    Chain ID: {config.chain_id}")
            print(f"    Latest block: {block}\n")

        except Exception as e:

            print(f"  ✗ {config.name}")
            print(f"    Error: {e}\n")


if __name__ == "__main__":
    test_all_evm_chains()