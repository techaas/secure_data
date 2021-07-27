import datetime
import hashlib
import json
import sys
from base64 import urlsafe_b64decode, urlsafe_b64encode

from Crypto.Cipher import AES, PKCS1_OAEP
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from Crypto.Util.Padding import pad, unpad
from Crypto.Signature import pkcs1_15

with open('private.pem', 'rb') as f:
    private_pem = f.read()
    private_key = RSA.import_key(private_pem)

with open ('data.txt', 'rt') as f:
    data = urlsafe_b64decode(f.read())

private_cipher = PKCS1_OAEP.new(private_key)
message = private_cipher.decrypt(data).decode("utf-8")
print(message)
config = json.loads(message)

key = urlsafe_b64decode(config['k'])
iv = urlsafe_b64decode(config['v'])
cipher = AES.new(key, AES.MODE_CBC, iv)

with open ('crypto_data.jpg', 'rb') as f:
    data = f.read()

try:
    pt = unpad(cipher.decrypt(data), AES.block_size)

    ver = pt[:1]
    print('ver: {}'.format(ver[0]))

    dt = pt[1:9]
    dti = int.from_bytes(dt, byteorder='big')
    dtn = datetime.datetime.fromtimestamp(dti / (1000 * 1000))
    print(dtn)

    with open ('output.jpg', 'wb') as f:
        f.write(pt[9:])

    m = hashlib.sha256()
    m.update(pt[9:])
    print(m.hexdigest())

except:
    print(sys.exc_info())
