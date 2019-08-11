#!/usr/bin/env python3
import sys
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

src = sys.argv[1]
dst = sys.argv[2]
key = sys.argv[3]

with open(key, 'rb') as fp:
    private_key = RSA.importKey(fp.read())
    signer = PKCS1_v1_5.new(private_key)

    digest = SHA256.new()
    with open(src, 'rb') as fp:
        data = fp.read(65536)
        while data:
            digest.update(data)
            data = fp.read(65536)

    sig = signer.sign(digest)
    with open(dst, 'wb') as fp:
        fp.write(sig)
