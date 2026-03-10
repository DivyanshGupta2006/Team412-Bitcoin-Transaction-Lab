from bitcoin.rpc import RawProxy

# --- Configuration ---
rpc_user = "user"
rpc_password = "password"
# Note the addition of /wallet/test_wallet at the end of the URL
proxy = RawProxy(service_url=f"http://{rpc_user}:{rpc_password}@127.0.0.1:18443/wallet/test_wallet")

def execute_part_2():
    print("==================================================================")
    print("ASSIGNMENT PART 2: SEGWIT (P2SH-P2WPKH) TRANSACTION WORKFLOW")
    print("==================================================================")

    # 1. Generate SegWit Addresses (P2SH-wrapped)
    print("\n[STEP 1: GENERATING SEGWIT ADDRESSES]")
    # We use 'p2sh-segwit' as required by the assignment [cite: 104, 1486]
    addr_ap = proxy.getnewaddress("A_prime", "p2sh-segwit")
    addr_bp = proxy.getnewaddress("B_prime", "p2sh-segwit")
    addr_cp = proxy.getnewaddress("C_prime", "p2sh-segwit")
    print(f"-> Created Address A': {addr_ap}")
    print(f"-> Created Address B': {addr_bp}")
    print(f"-> Created Address C': {addr_cp}")

    # 2. Fund Address A'
    print("\n[STEP 2: FUNDING ADDRESS A']")
    # In Part 2, we can simply send funds from our wallet to A' [cite: 105]
    proxy.sendtoaddress(addr_ap, 10.0)
    proxy.generatetoaddress(1, addr_ap)
    print(f"-> Address A' funded with 10 BTC via internal transfer.")

    # 3. Transaction A' -> B'
    print("\n[STEP 3: CREATING TRANSACTION A' -> B']")
    utxo = proxy.listunspent(1, 9999, [addr_ap])[0]
    inputs = [{"txid": utxo['txid'], "vout": utxo['vout']}]
    outputs = {addr_bp: 5.0, addr_ap: 4.999} 
    
    raw_tx_apbp = proxy.createrawtransaction(inputs, outputs)
    signed_tx_apbp = proxy.signrawtransactionwithwallet(raw_tx_apbp)
    txid_apbp = proxy.sendrawtransaction(signed_tx_apbp['hex'])
    proxy.generatetoaddress(1, addr_ap)
    print(f"-> Success: TXID A' -> B' is: {txid_apbp}")

    # 4. Transaction B' -> C'
    print("\n[STEP 4: CREATING TRANSACTION B' -> C']")
    utxo_b = proxy.listunspent(1, 9999, [addr_bp])[0]
    inputs_bpcp = [{"txid": utxo_b['txid'], "vout": utxo_b['vout']}]
    outputs_bpcp = {addr_cp: 2.0, addr_bp: 2.999}
    
    raw_tx_bpcp = proxy.createrawtransaction(inputs_bpcp, outputs_bpcp)
    signed_tx_bpcp = proxy.signrawtransactionwithwallet(raw_tx_bpcp)
    txid_bpcp = proxy.sendrawtransaction(signed_tx_bpcp['hex'])
    proxy.generatetoaddress(1, addr_ap)
    print(f"-> Success: TXID B' -> C' is: {txid_bpcp}")

    # --- Analysis Section for Report ---
    print("\n" + "="*60)
    print("ANALYSIS FOR REPORT (SEGWIT P2SH-P2WPKH)")
    print("="*60)

    decoded_bpcp = proxy.decoderawtransaction(proxy.getrawtransaction(txid_bpcp))
    
    # Analyze the Witness Data [cite: 1339, 1502]
    print(f"1. WITNESS DATA (The 'Segregated' Signatures):")
    # This field did not exist in Part 1! [cite: 1394-1395]
    witness = decoded_bpcp['vin'][0]['txinwitness']
    print(f"   Signature: {witness[0]}")
    print(f"   Public Key: {witness[1]}")
    
    # Analyze the scriptSig (Witness Program) [cite: 1244, 1468]
    print(f"\n2. REDEEM SCRIPT (scriptSig):")
    print(f"   ASM: {decoded_bpcp['vin'][0]['scriptSig']['asm']}")
    print("   Note: This is just a 'Witness Program' that points to the actual signatures above.")

    # Size Metrics for Part 3 [cite: 1340, 1492]
    print(f"\n3. SEGWIT SIZE METRICS:")
    print(f"   - Total Bytes (Size): {decoded_bpcp['size']}")
    print(f"   - Virtual Size (VSize): {decoded_bpcp['vsize']}")
    print(f"   - Weight: {decoded_bpcp['weight']}")
    print("   CRITICAL OBSERVATION: VSize is now SMALLER than Size because of the 75% witness discount!")
    print("==================================================================")

execute_part_2()