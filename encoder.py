from __future__ import unicode_literals

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

from os.path import join, dirname, realpath, splitext

def string_normalization(filename):
    filename = filename + '.pub.pem' if not filename.endswith('.pub.pem') else filename
    return join(dirname(realpath(__file__)), filename)

def encoder(message, public_key):
    public_key = string_normalization(public_key)
    with open(public_key, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
        
    return public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )