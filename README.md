# Bitcoin Transaction Lab – Legacy & SegWit Transactions

**Course:** CS216 – Introduction to Blockchain  
**Instructor:** Prof. Subhra Mazumdar  
**Institute:** Indian Institute of Technology Indore  

This repository contains the implementation of Bitcoin transactions using **Legacy (P2PKH)** and **SegWit (P2SH-P2WPKH)** address formats using **Python RPC interaction with Bitcoin Core (`bitcoind`)**.

The assignment demonstrates how to:

- Connect to a Bitcoin node using RPC
- Create and manage wallets
- Generate Bitcoin addresses
- Construct raw transactions
- Sign transactions using wallet keys
- Broadcast transactions to the network
- Decode and analyze transaction scripts
- Compare transaction size metrics

All experiments are performed using **Bitcoin Regtest mode**.

---

# Team Information

**Team ID:** 412  

| Name | Roll Number |
|-----|-----|
| Divyansh Gupta | 240041015 |
| Harsh Mahajan | 240001034 |
| Darsh Chaudhary | 240004014 |
| Akarsh J | 240002007 |

---

# Repository Structure

```
.
├── part1_legacy.py
|── bitcoin.conf
|── Team_4121_ReportFinal.Pdf
├── part2_segwit.py
├── requirements.txt
└── README.md
```

**Files**
- `bitcoin.conf` →File is the primary configuration bridge between the Bitcoin Core daemon (bitcoind) and the Python automation scripts
- `part1_legacy.py` → Implementation of Legacy **P2PKH** transaction workflow  
- `part2_segwit.py` → Implementation of **P2SH-P2WPKH SegWit** transaction workflow  
- `requirements.txt` → Python dependencies required to run the scripts  

---

# Requirements

## Software

- Bitcoin Core
- Python 3.8+
- Bitcoin CLI (`bitcoin-cli`)

---

## Python Dependencies

Install dependencies using:

```bash
pip install -r requirements.txt
```

Contents of `requirements.txt`:

```
python-bitcoinlib
python-bitcoinrpc
```

---

# Bitcoin Core Setup

Run Bitcoin Core in **regtest mode**.

Edit the **bitcoin.conf** file:

```
regtest=1
rpcuser=user
rpcpassword=password
server=1

# Assignment Fee Requirements
paytxfee=0.0001
fallbackfee=0.0002
mintxfee=0.00001
txconfirmtarget=6
```

---

# Start the Bitcoin Node

Start the daemon:

```bash
bitcoind -regtest -daemon
```

Verify the node is running:

```bash
bitcoin-cli -regtest getblockchaininfo
```

---

# RPC Configuration Used in Scripts

The scripts connect to the Bitcoin daemon using the following RPC endpoint:

```
http://user:password@127.0.0.1:18443/wallet/test_wallet
```

---

# Part 1 – Legacy Transactions (P2PKH)

File: `part1_legacy.py`

This script demonstrates the lifecycle of **Legacy Bitcoin transactions**.

## Workflow

1. Create or load a wallet
2. Generate three legacy addresses
   - Address A (Sender)
   - Address B (Intermediate)
   - Address C (Receiver)
3. Mine **101 blocks** to fund Address A
4. Create a raw transaction **A → B**
5. Use the UTXO from the first transaction to create **B → C**
6. Decode transactions to analyze scripts
7. Compare transaction size metrics

## Run

```bash
python part1_legacy.py
```

---

# Part 2 – SegWit Transactions (P2SH-P2WPKH)

File: `part2_segwit.py`

This script implements the same workflow using **SegWit addresses wrapped inside P2SH**.

## Workflow

1. Generate SegWit addresses
   - A'
   - B'
   - C'
2. Fund Address A'
3. Create transaction **A' → B'**
4. Create transaction **B' → C'**
5. Decode transactions
6. Extract witness data
7. Compare transaction size metrics

## Run

```bash
python part2_segwit.py
```

---

# Script Analysis

## Legacy Transaction Script

Locking Script (`scriptPubKey`):

```
OP_DUP OP_HASH160 <PubKeyHash> OP_EQUALVERIFY OP_CHECKSIG
```

Unlocking Script (`scriptSig`):

```
<Signature> <PublicKey>
```

Validation occurs by concatenating `scriptSig` and `scriptPubKey` and executing them in the **Bitcoin Script engine**.

---

## SegWit Transaction Structure

SegWit separates signature data into a **Witness field**.

Structure:

- `scriptSig` contains the **redeem script**
- Signatures and public keys are stored in **txinwitness**

Example witness stack:

```
Witness:
<Signature>
<PublicKey>
```

---

# Transaction Size Comparison

| Metric | Legacy (P2PKH) | SegWit (P2SH-P2WPKH) |
|------|------|------|
| Physical Size | ~225 bytes | ~247 bytes |
| Virtual Size | ~225 vB | ~166 vB |
| Weight | ~900 WU | ~661 WU |

### Observation

Although SegWit transactions may have a slightly larger raw byte size, their **virtual size (vBytes)** is significantly smaller because **witness data receives a weight discount**.  
This allows more transactions to fit inside a block.

---

# Key Concepts Demonstrated

- UTXO based transaction model
- Raw transaction construction
- Bitcoin Script locking and unlocking mechanisms
- Interaction with Bitcoin Core using RPC
- SegWit witness data structure
- Transaction size metrics (size, vsize, weight)
- Comparison between Legacy and SegWit transactions

---

# References

- Bitcoin Core Documentation  
- BIP 16 – Pay to Script Hash (P2SH)  
- BIP 141 – Segregated Witness (SegWit)  
- Learning Bitcoin from the Command Line
