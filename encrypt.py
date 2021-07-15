import hashlib
from Crypto.Cipher import AES
import random
import sys
import getpass

description = """
version: 1.3
hash: sha3-256
encryption: AES
"""
description = description.strip()

if len(sys.argv) != 3:
    print(f"usage: python3 {sys.argv[0]} <input file> <output file>")
    exit()

source_file = sys.argv[0]
input_file = sys.argv[1]
output_file = sys.argv[2]

MOD = 1<<256

def confirm(question):
    print(question)
    print("> ", end="")

def write_number(f, val, blen):
    f.write(val.to_bytes(blen, "little"))

def write_int(f, val):
    write_number(f, val, 4)

def write_str(f, s):
    s = s.encode("utf-8")
    write_int(f, len(s))
    f.write(s)

def product(bit, ans):
    ret = 1
    for i in range(len(ans)):
        if (bit>>i) % 2 == 1:
            ret *= ans[i]
            ret %= MOD
    return ret

def calc_coefficients(answers, passing_grade, key):

    N = len(answers)
    degree = N - passing_grade + 1

    answers = list(map(lambda x: (-x)%MOD, answers))

    coefficients = [0] * (2**N)
    coefficients[0] = key

    for bit in range(2**N):

        popcount = 0
        for i in range(N):
            if (bit>>i) % 2 == 1:
                popcount += 1

        if popcount != degree:
            continue

        sub = 0

        c = random.randrange(MOD)

        while True:

            sub = (sub-1) & bit

            coefficients[bit&(~sub)] += product(sub, answers) * c
            coefficients[bit&(~sub)] %= MOD

            if sub == 0:
                break

    return coefficients

questions = []
while True:
    confirm("質問を入力してください。質問を追加しない場合はそのままEnterを押してください。")
    q = input()
    if q == "":
        break
    questions.append(q)

n = len(questions)
answers = [None] * n

print("答えを入力してください。")

for i in range(n):
    print(questions[i])
    answers[i] = getpass.getpass("> ")

print("それぞれもう一度答えを入力してください。")

for i in range(n):
    print(questions[i])
    ans = getpass.getpass("> ")
    if ans != answers[i]:
        print("1回目の答えと異なります。もう一度入力してください。")
        ans2 = getpass.getpass("> ")
        if ans2 != answers[i]:
            if ans2 == ans:
                answers[i] = ans2
                print("答えを更新しました。")
            else:
                print("答えが一致しませんでした。")
                exit()

confirm(f"{n}個の質問を登録しました。何問正解で復号可能にしますか？")
passing_grade = int(input())

hash_values = []
key = random.randint(0, 1<<256)

for ans in answers:
    a = hashlib.sha3_256(ans.encode('utf-8'))
    a = int(a.hexdigest(), 16)
    hash_values.append(a)

coeff = calc_coefficients(hash_values, passing_grade, key)

with open(input_file, mode="rb") as f:
    raw = f.read()

    key = key.to_bytes(32, "little")

    iv = random.randint(0, 1<<128).to_bytes(16, "little")

    cipher = AES.new(key, AES.MODE_CBC, iv)

with open(output_file, mode='wb') as f:

    # ファイルシグネチャ + バージョン情報
    f.write(b"MSQ ")
    write_str(f, description)

    # 質問とその個数
    write_int(f, n)
    for i in range(n):
        write_str(f, questions[i])

    # 0 でない係数の個数
    cnt = 0
    for bit in range(1<<n):
        if coeff[bit] != 0:
            cnt += 1
    write_int(f, cnt)

    # 係数
    for bit in range(1<<n):
        if coeff[bit] != 0:
            write_int(f, bit)
            write_number(f, coeff[bit], 32)

    # 初期ベクトル
    f.write(iv)

    # データの実際のサイズ
    write_int(f, len(raw))

    # データサイズを 16 の倍数にして暗号化する
    if len(raw) % 16 != 0:
        raw += int().to_bytes(16 - len(raw) % 16, "little")
    f.write(cipher.encrypt(raw))

