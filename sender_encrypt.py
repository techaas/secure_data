# Copyright(c) 2021 TECHaas.com, all rights reserved.
#

import datetime
import hashlib
import json
from base64 import urlsafe_b64encode

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

f_ver = bytes.fromhex('01')

with open ('test_data.jpg', 'rb') as f:
    data = f.read()

m = hashlib.sha256()
m.update(data)
print(m.hexdigest())

# AES鍵データの準備

ct = datetime.datetime.now()
print(ct)
cti = int(ct.timestamp() * 1000 * 1000)
print(cti)
time_val = cti.to_bytes(8, 'big')

data = f_ver + time_val + data
m = hashlib.sha256()
m.update(data)

# AES暗号化と保存

cipher = AES.new(m.digest(), AES.MODE_CBC)
ct_bytes = cipher.encrypt(pad(data, AES.block_size))

with open ('crypto_data.jpg', 'wb') as f:
    f.write(ct_bytes)

# 鍵データを RSA 暗号で保存
key = urlsafe_b64encode(m.digest()).decode('utf-8')
iv = urlsafe_b64encode(cipher.iv).decode('utf-8')
message = json.dumps({'k':key,'v':iv})
print(message)

with open('public.pem', 'br') as f:
    public_pem = f.read()
    public_key = RSA.import_key(public_pem)

public_cipher = PKCS1_OAEP.new(public_key)
ciphertext = public_cipher.encrypt(message.encode())

with open ('data.txt', 'wb') as f:
    f.write(urlsafe_b64encode(ciphertext))


