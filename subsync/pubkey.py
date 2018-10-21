import config
from error import Error
import os
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5

_verifier = None


def getPublicKey():
    for path in config.keypaths:
        if os.path.isfile(path):
            with open(path, 'rb') as fp:
                return RSA.importKey(fp.read())
    raise Error(_('Cannot load public key'), paths=config.keypaths)


def getVerifier():
    global _verifier
    if not _verifier:
        key = getPublicKey()
        _verifier = PKCS1_v1_5.new(key)
    return _verifier

