from subsync import config

_pubkey = None


def verify_cryptography(hash, sig):
    from cryptography.hazmat.backends import default_backend
    from cryptography.hazmat.primitives import serialization, hashes
    from cryptography.hazmat.primitives.asymmetric import padding, utils

    global _pubkey
    if not _pubkey:
        with open(config.keypath, 'rb') as fp:
            _pubkey = serialization.load_pem_public_key(fp.read(), backend=default_backend())
    _pubkey.verify(sig, hash.digest(), padding.PKCS1v15(), utils.Prehashed(hashes.SHA256()))


def verify_crypto(hash, sig):
    from Crypto.PublicKey import RSA
    from Crypto.Signature import PKCS1_v1_5

    global _pubkey
    if not _pubkey:
        with open(config.keypath, 'rb') as fp:
            _pubkey = RSA.importKey(fp.read())

    verifier = PKCS1_v1_5.new(_pubkey)
    assert( verifier.verify(hash, sig) )


try:
    import Crypto
    from Crypto.Hash import SHA256
    verify = verify_crypto
    sha256 = SHA256.new

except ImportError:
    import hashlib
    verify = verify_cryptography
    sha256 = hashlib.sha256
