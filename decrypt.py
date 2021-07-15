import hashlib
from Crypto.Cipher import AES
import random
import sys
import getpass

if len(sys.argv) != 3:
    print(f"usage: python3 {sys.argv[0]} <input file> (<output file> | -)")
    exit()

input_file = sys.argv[1]
output_file = sys.argv[2]

MOD = 1<<256

def read_number(f, blen):
    return int.from_bytes(f.read(blen), "little")

def read_int(f):
    return read_number(f, 4) 

def read_str(f):
    l = read_int(f)
    return f.read(l).decode("utf-8")

with open(input_file, mode='rb') as f:
    signature = f.read(4).decode("ASCII")
    if signature != "MSQ ":
        print("Not supported")
        exit()

    description = read_str(f)
    print(description)
    print()

    n = read_int(f)

    questions = []
    answers = [""] * n
    hash_values = [0] * n
    coeff = [0] * (1<<n)

    for i in range(n):
        questions.append(read_str(f))

    cnt = read_int(f)
    for i in range(cnt):
        bit = read_int(f)
        c = read_number(f, 32)
        coeff[bit] = c

    iv = f.read(16)

    size = read_int(f)
    b = f.read()

def product(bit, ans):
    ret = 1
    for i in range(len(ans)):
        if (bit>>i) % 2 == 1:
            ret *= ans[i]
            ret %= MOD
    return ret

for i in range(n):
    print(questions[i])
    answers[i] = getpass.getpass("> ")

for i in range(n):
    a = hashlib.sha3_256(answers[i].encode('utf-8'))
    a = int(a.hexdigest(), 16)
    hash_values[i] = a

key = 0
for bit in range(2**n):
    key += product(bit, hash_values) * coeff[bit]
    key %= MOD

key = key.to_bytes(32, "little")

cipher = AES.new(key, AES.MODE_CBC, iv)
decoded = cipher.decrypt(b)

if output_file == "-":
    print(decoded[0:size].decode("utf-8"))
else:
    with open(output_file, "wb") as f:
        f.write(decoded[0:size])
