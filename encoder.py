from __future__ import unicode_literals

import os
import json
import binascii

from random import SystemRandom
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

from os.path import join, dirname, realpath, splitext

from dotenv import load_dotenv
load_dotenv(verbose=False)

def string_normalization(filename):
    filename = filename + '.pem' if not filename.endswith('.pem') else filename
    return join(dirname(realpath(__file__)), filename)

def sym_encoder(message, keyname):
    # if not password:
    #     alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    #     password = "".join(SystemRandom().choice(alphabet) for _ in range(40))
        
    # password_bytes = password.encode('utf-8')

    # # GENERATE random salt (needed for PBKDF2HMAC)
    # salt = os.urandom(64)

    # # DERIVE key (from password and salt)
    # kdf = PBKDF2HMAC(
    #     algorithm=hashes.SHA512(),
    #     length=32,
    #     salt=salt,
    #     iterations=10000,
    #     backend=default_backend()
    # )
    # key = kdf.derive(password_bytes)

    # # GENERATE random nonce (number used once)
    # nonce = os.urandom(12)

    # # ENCRYPTION
    # aesgcm = AESGCM(key)
    # cipher_text_bytes = aesgcm.encrypt(
    #     nonce=nonce,
    #     data=message.encode('utf-8'),
    #     associated_data=None
    # )
    # # CONVERSION of raw bytes to BASE64 representation
    # cipher_text = base64.urlsafe_b64encode(cipher_text_bytes)
    
    # # Dumping the data here will pass it as a string, which we need to encrypt everything asymetrically
    # return {
    #     'key': key,
    #     'nonce': nonce,
    #     'data_encrypted': cipher_text
    # }
    full_keyname = string_normalization(keyname)
    with open(full_keyname, 'rb') as f:
        key = f.read()
    
    # key = Fernet.generate_key()
    enc = Fernet(key)
    encrypted = json.dumps(enc.encrypt(message)).encode('utf-8')
    
    return {
        'key':keyname,
        'data_encrypted':encrypted
    }
    
def asym_encoder(package, public_key):
    public_key = string_normalization(public_key)
    with open(public_key, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
        
    encrypted = public_key.encrypt(
        package,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted

def encoder(message, key):
    sym_encrypted = sym_encoder(message, key) # This encrypts the message as part of the payload
    # key = base64.b64encode(sym_encrypted['aes_key'])
    # # sym_package = json.dumps({
    # #     'key':key,
    # #     'nonce':nonce
    # # })
    # # The encrypted data
    # data_encrypted = sym_encrypted['data_encrypted']
    # sym_package_encrypted = asym_encoder(key, public_key)
    # print "Type of encoding: ",type(sym_package_encrypted)
    return sym_encrypted
    