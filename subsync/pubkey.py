from subsync import config
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

_verifier = None


def getPublicKey():
    with open(config.keypath, 'rb') as fp:
        return RSA.importKey(fp.read())


def getVerifier():
    global _verifier
    if not _verifier:
        key = getPublicKey()
        _verifier = PKCS1_v1_5.new(key)
    return _verifier

