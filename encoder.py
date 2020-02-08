from __future__ import unicode_literals

import os
import json

import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.fernet import Fernet

from os.path import join, dirname, realpath, splitext

from dotenv import load_dotenv
load_dotenv(verbose=False)

def string_normalization(filename):
    filename = filename + '.pub.pem' if not filename.endswith('.pub.pem') else filename
    return join(dirname(realpath(__file__)), filename)

def sync_encoder(d_string):
    message = d_string.encode('ascii')
    assert type(message) == bytes
    
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted = cipher_suite.encrypt(message)
    
    return {
        'aes_string':key.decode(),
        'data_encrypted':encrypted.decode()
    }
    
def async_encoder(package, public_key):
    data_package = package.encode('ascii')
    public_key = string_normalization(public_key)
    with open(public_key, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )        
        
    encrypted = public_key.encrypt(
        data_package,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.standard_b64encode(encrypted).decode()

def encoder(message, public_key):
    sync_encrypted = sync_encoder(message) # This encrypts the message as part of the payload
    aes_string = sync_encrypted['aes_string']
    
    # The encrypted data
    data_encrypted = sync_encrypted['data_encrypted']
    aes_encrypted = async_encoder(aes_string, public_key)
    
    return {
        'key': public_key,
        'aes_encrypted': aes_encrypted,
        'data_encrypted': data_encrypted
    }
    