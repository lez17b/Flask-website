"""
Name: Luciano Zavala
Date: 10/03/2021
Assignment: Module 6: Encrypt Data in database
Due Date: 10/03/2021
About this project: The goal of this project is to develop a frontend application that will
interact with the Agent database for a small scale real-world application using third-party
Python libraries (Flask, sqlite3, Crypto.Cipher, Pandas) . In this script, we have the code
for our flask website. The application has added an role based login system and the database
has been encrypted.
Assumptions: N/A
All work below was performed by Luciano Zavala
"""

import string,base64

##################################
#      Encryption class          #
# Taken from the lectures of the #
#    class made by Dr. Works     #
##################################
from Crypto.Cipher import AES


class AESCipher(object):

    # Constructor
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

    # Encryption method
    def encrypt(self, raw):
        self.cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        ciphertext = self.cipher.encrypt(raw)
        encoded = base64.b64encode(ciphertext)
        return encoded

    # Decryption method
    def decrypt(self, raw):
        self.cipher = AES.new(self.key, AES.MODE_CFB, self.iv)
        decoded = base64.b64decode(raw)
        decrypted = self.cipher.decrypt(decoded)
        return str(decrypted, 'utf-8')


key = b'BLhgpCL81fdLBk23HkZp8BgbT913cqt0'
iv = b'OWFJATh1Zowac2xr'

cipher = AESCipher(key, iv)

