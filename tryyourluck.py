#
# ☮ mvxim
# This, obviously, won't actually gather any useful data. Proof of concept.
# It generates a random seed, then a random private and public key.
# It checks the public key balance. If > 0 we save it, else, it's discarded.
# You need the bip39 seed list: https://github.com/bitcoin/bips/blob/master/bip-0039/english.txt
# Run with: python3 generate_addresses.py
#  _     _                       
# | |   | |                      
# | |__ | |_ ___ __ _  ___ _ __  
# | '_ \| __/ __/ _` |/ _ \ '_ \ 
# | |_) | || (_| (_| |  __/ | | |
# |_.__/ \__\___\__, |\___|_| |_|
#                __/ |           
#               |___/         
#

import os
import random
import requests
import hashlib

def generate_address(seed):
    # Use seed to generate a private key
    private_key = hashlib.sha256(seed.encode()).hexdigest()
    # Use private key to generate a public address
    public_address = hashlib.sha256(private_key.encode()).hexdigest()
    return public_address

def check_balance(address):
    url = f"https://blockchain.info/q/addressbalance/{address}"
    response = requests.get(url)
    balance_text = response.text
    try:
        balance = int(balance_text)
    except ValueError:
        balance = 0
    return balance

def save_key(private_key):
    with open("private_keys.txt", "a") as file:
        file.write(private_key + "\n")
        
def save_attempts(seed, private_key, balance):
    with open("attempts.csv", "a") as file:
        file.write(f"{seed},{private_key},{balance}\n")

with open("bip39.txt") as file:
    words = file.read().splitlines()

word_count = 24
for i in range(1000):
    seed_words = random.sample(words, word_count)
    seed = ' '.join(seed_words)
    address = generate_address(seed)
    balance = check_balance(address)
    if balance > 0:
        save_key(address)
        save_attempts(seed, address, balance)
        print(f"Found address with balance {balance} at iteration {i + 1}. Seed: '{seed}', Address: '{address}'")
    else:
        save_attempts(seed, address, balance)
        print(f"No balance found at iteration {i + 1}. Seed: '{seed}', Address: '{address}'")
