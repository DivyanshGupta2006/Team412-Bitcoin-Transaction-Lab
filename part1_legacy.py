from bitcoin.rpc import RawProxy

# --- Configuration ---
rpc_user = "user"
rpc_password = "password"
# Matches the wallet created in previous steps
proxy = RawProxy(service_url=f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/lab_wallet")


def execute_part_1_with_narrative():
    print("==================================================================")
    print("ASSIGNMENT PART 1: LEGACY (P2PKH) TRANSACTION WORKFLOW")
    print("==================================================================")

    # 1. Setup Wallet
    print("\n[STEP 1: WALLET INITIALIZATION]")
    try:
        proxy.createwallet("lab_wallet")
        print("-> Action: Created a new wallet named 'lab_wallet'.")
    except:
        print("-> Action: 'lab_wallet' already exists. Loading it into the daemon.")

    # 2. Generate Addresses
    print("\n[STEP 2: ADDRESS GENERATION]")
    addr_a = proxy.getnewaddress("Address_A", "legacy")
    addr_b = proxy.getnewaddress("Address_B", "legacy")
    addr_c = proxy.getnewaddress("Address_C", "legacy")
    print(f"-> Created Address A (Sender): {addr_a}")
    print(f"-> Created Address B (Intermediate): {addr_b}")
    print(f"-> Created Address C (Final Receiver): {addr_c}")
    print("Note: These are P2PKH addresses (Legacy format) used for Part 1.")

    # 3. Fund via Mining
    print("\n[STEP 3: FUNDING VIA MINING]")
    print("-> Action: Mining 101 blocks to Address A.")
    print("-> Why: Coinbase rewards require 100 confirmations before they can be spent.")
    proxy.generatetoaddress(101, addr_a)
    balance = proxy.getbalance()
    print(f"-> Current Wallet Balance: {balance} BTC (Confirmed and Spendable).")

    # 4. Transaction A -> B: Broadcast and Confirm
    print("\n[STEP 4: CREATING TRANSACTION A -> B]")
    utxo = proxy.listunspent(1, 9999, [addr_a])[0]
    print(f"-> Input: Selecting UTXO from A (TXID: {utxo['txid']})")

    inputs = [{"txid": utxo['txid'], "vout": utxo['vout']}]
    outputs = {addr_b: 10.0, addr_a: 39.999}

    raw_tx_ab = proxy.createrawtransaction(inputs, outputs)
    signed_tx_ab = proxy.signrawtransactionwithwallet(raw_tx_ab)

    # BROADCASTING
    txid_ab = proxy.sendrawtransaction(signed_tx_ab['hex'])
    # ADDING ONE BLOCK FOR CONFIRMATION
    proxy.generatetoaddress(1, addr_a)
    print(f"-> Action: Signed and broadcasted Transaction A -> B.")
    print(f"-> Success: TXID for A -> B is: {txid_ab}")

    # 5. Transaction B -> C: Broadcast and Confirm
    print("\n[STEP 5: CREATING TRANSACTION B -> C]")
    print("-> Logic: This transaction will spend the 10 BTC received by Address B.")
    utxo_b = proxy.listunspent(1, 9999, [addr_b])[0]
    inputs_bc = [{"txid": utxo_b['txid'], "vout": utxo_b['vout']}]
    outputs_bc = {addr_c: 5.0, addr_b: 4.999}

    raw_tx_bc = proxy.createrawtransaction(inputs_bc, outputs_bc)
    signed_tx_bc = proxy.signrawtransactionwithwallet(raw_tx_bc)

    # BROADCASTING
    txid_bc = proxy.sendrawtransaction(signed_tx_bc['hex'])
    # ADDING ONE BLOCK FOR CONFIRMATION
    proxy.generatetoaddress(1, addr_a)
    print(f"-> Success: TXID for B -> C is: {txid_bc}")

    # --- Analysis Section for Report ---
    print("\n" + "=" * 60)
    print("ANALYSIS FOR REPORT (LEGACY P2PKH)")
    print("=" * 60)

    # Locking Script Analysis (extracted from output of A->B)
    # Using gettransaction hex because the TX is now confirmed in a block
    decoded_ab = proxy.decoderawtransaction(proxy.gettransaction(txid_ab)['hex'])
    lock_script = decoded_ab['vout'][0]['scriptPubKey']['asm']
    print(f"\n1. LOCKING SCRIPT (from A -> B):")
    print(f"   ASM: {lock_script}")
    print("   Role: This is the 'Challenge'. It locks the 10 BTC to Address B's public key hash.")

    # Unlocking Script Analysis (extracted from input of B->C)
    decoded_bc = proxy.decoderawtransaction(proxy.gettransaction(txid_bc)['hex'])
    unlock_script = decoded_bc['vin'][0]['scriptSig']['asm']
    print(f"\n2. UNLOCKING SCRIPT (from B -> C):")
    print(f"   ASM: {unlock_script}")
    print("   Role: This is the 'Response'. It contains the signature and public key from Address B.")

    # Size Metrics
    print(f"\n3. SIZE COMPARISON:")
    print(f"   - Total Bytes (Size): {decoded_bc['size']}")
    print(f"   - Virtual Size (VSize): {decoded_bc['vsize']}")
    print(f"   - Weight: {decoded_bc['weight']}")
    print("   Note: In Legacy, Size and VSize are always identical.")


if __name__ == "__main__":
    execute_part_1_with_narrative()