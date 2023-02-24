#
# ☮ mvxim
# python3 cipher.py -e -a abcdefghijklmnopqrstuvwxyz -s 1 -m "the message"
# python3 cipher.py -d -a abcdefghijklmnopqrstuvwxyz -s 1 -m "the cipher message"
# To use run the command above.
# You can change the alphabet sequence and shift number for security.
# Validate on: https://cryptii.com/pipes/caesar-cipher
#       _       _
#      (_)     | |
#   ___ _ _ __ | |__   ___ _ __
#  / __| | '_ \| '_ \ / _ \ '__|
# | (__| | |_) | | | |  __/ |
#  \___|_| .__/|_| |_|\___|_|
#        | |
#        |_|
#

import argparse

def caesar_cipher(message, alphabet, shift, decode=False):
    if decode:
        shift = -shift
    shifted_alphabet = alphabet[shift:] + alphabet[:shift]
    table = str.maketrans(alphabet, shifted_alphabet)
    return message.translate(table)

parser = argparse.ArgumentParser(description='Encode or decode text using a Caesar cipher.')
parser.add_argument('-a', '--alphabet', type=str, default='abcdefghijklmnopqrstuvwxyz', help='Alphabet used for encoding or decoding.')
parser.add_argument('-s', '--shift', type=int, default=3, help='Number of characters to shift.')
parser.add_argument('-e', '--encode', action='store_true', help='Encode the input message.')
parser.add_argument('-d', '--decode', action='store_true', help='Decode the input message.')
parser.add_argument('-m', '--message', type=str, required=True, help='Message to encode or decode.')

args = parser.parse_args()

if args.encode and args.decode:
    print("Error: cannot encode and decode at the same time.")
elif not args.encode and not args.decode:
    print("Error: must specify either -e or -d.")
else:
    message = args.message
    alphabet = args.alphabet
    shift = args.shift
    decode = args.decode

    if args.encode:
        encoded_message = caesar_cipher(message, alphabet, shift)
        print(encoded_message)
    else:
        decoded_message = caesar_cipher(message, alphabet, shift, decode=True)
        print(decoded_message)
