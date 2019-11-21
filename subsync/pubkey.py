from subsync import config
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, utils

_pubkey = None


def getPublicKey():
    global _pubkey
    if not _pubkey:
        with open(config.keypath, 'rb') as fp:
            _pubkey = serialization.load_pem_public_key(fp.read(), backend=default_backend())
    return _pubkey


def verify(hash, sig):
    getPublicKey().verify(sig, hash.digest(), padding.PKCS1v15(), utils.Prehashed(hashes.SHA256()))


def getVerifier():
    global _verifier
    if not _verifier:
        key = getPublicKey()
        _verifier = PKCS1_v1_5.new(key)
    return _verifier

