from bitcoin.rpc import RawProxy

# --- Configuration ---
rpc_user = "user"
rpc_password = "password"
# Ensure the wallet name matches your WSL setup (e.g., lab_wallet)
proxy = RawProxy(service_url=f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/lab_wallet")


def execute_part_2():
    print("==================================================================")
    print("ASSIGNMENT PART 2: SEGWIT (P2SH-P2WPKH) TRANSACTION WORKFLOW")
    print("==================================================================")

    # 1. Generate SegWit Addresses (P2SH-wrapped)
    print("\n[STEP 1: GENERATING SEGWIT ADDRESSES]")
    addr_ap = proxy.getnewaddress("A_prime", "p2sh-segwit")
    addr_bp = proxy.getnewaddress("B_prime", "p2sh-segwit")
    addr_cp = proxy.getnewaddress("C_prime", "p2sh-segwit")
    print(f"-> Created Address A': {addr_ap}")
    print(f"-> Created Address B': {addr_bp}")
    print(f"-> Created Address C': {addr_cp}")

    # 2. Fund Address A'
    print("\n[STEP 2: FUNDING ADDRESS A']")
    proxy.sendtoaddress(addr_ap, 10.0)
    # Confirmation for funding
    proxy.generatetoaddress(1, addr_ap)
    print(f"-> Action: Mining 1 block to confirm funding transfer.")
    print(f"-> Address A' funded with 10 BTC via internal transfer.")

    # 3. Transaction A' -> B'
    print("\n[STEP 3: CREATING TRANSACTION A' -> B']")
    utxo = proxy.listunspent(1, 9999, [addr_ap])[0]
    inputs = [{"txid": utxo['txid'], "vout": utxo['vout']}]
    outputs = {addr_bp: 5.0, addr_ap: 4.999}

    raw_tx_apbp = proxy.createrawtransaction(inputs, outputs)
    signed_tx_apbp = proxy.signrawtransactionwithwallet(raw_tx_apbp)

    # BROADCASTING
    txid_apbp = proxy.sendrawtransaction(signed_tx_apbp['hex'])
    # CONFIRMATION
    proxy.generatetoaddress(1, addr_ap)
    print(f"-> Action: Signed and broadcasted Transaction A' -> B'.")
    print(f"-> Confirmation: Mining 1 block to confirm A' -> B'.")
    print(f"-> Success: TXID A' -> B' is: {txid_apbp}")

    # 4. Transaction B' -> C'
    print("\n[STEP 4: CREATING TRANSACTION B' -> C']")
    print("-> Logic: This transaction will spend the 5 BTC received by Address B'.")
    utxo_b = proxy.listunspent(1, 9999, [addr_bp])[0]
    inputs_bpcp = [{"txid": utxo_b['txid'], "vout": utxo_b['vout']}]
    outputs_bpcp = {addr_cp: 2.0, addr_bp: 2.999}

    raw_tx_bpcp = proxy.createrawtransaction(inputs_bpcp, outputs_bpcp)
    signed_tx_bpcp = proxy.signrawtransactionwithwallet(raw_tx_bpcp)

    # BROADCASTING
    txid_bpcp = proxy.sendrawtransaction(signed_tx_bpcp['hex'])
    # CONFIRMATION
    proxy.generatetoaddress(1, addr_ap)
    print(f"-> Action: Signed and broadcasted Transaction B' -> C'.")
    print(f"-> Confirmation: Mining 1 block to confirm B' -> C'.")
    print(f"-> Success: TXID B' -> C' is: {txid_bpcp}")

    # --- Analysis Section for Report ---
    print("\n" + "=" * 60)
    print("ANALYSIS FOR REPORT (SEGWIT P2SH-P2WPKH)")
    print("=" * 60)

    # Use gettransaction to ensure we find the mined transaction
    tx_details = proxy.gettransaction(txid_bpcp)
    decoded_bpcp = proxy.decoderawtransaction(tx_details['hex'])

    # Analyze the Witness Data
    print(f"\n1. WITNESS DATA (The 'Segregated' Signatures):")
    witness = decoded_bpcp['vin'][0]['txinwitness']
    print(f"   Signature: {witness[0]}")
    print(f"   Public Key: {witness[1]}")
    print("   Role: This data is stored outside the base transaction to reduce weight.")

    # Analyze the scriptSig (Witness Program)
    print(f"\n2. REDEEM SCRIPT (scriptSig):")
    print(f"   ASM: {decoded_bpcp['vin'][0]['scriptSig']['asm']}")
    print("   Note: This is a Witness Program; the actual signatures are in the witness field.")

    # Size Metrics
    print(f"\n3. SEGWIT SIZE METRICS:")
    print(f"   - Total Bytes (Size): {decoded_bpcp['size']}")
    print(f"   - Virtual Size (VSize): {decoded_bpcp['vsize']}")
    print(f"   - Weight: {decoded_bpcp['weight']}")
    print("   CRITICAL OBSERVATION: VSize is smaller than Size because of the 75% witness discount.")


if __name__ == "__main__":
    execute_part_2()