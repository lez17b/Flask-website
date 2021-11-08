"""
Name: Luciano Zavala
Date: 11/07/2021
Assignment: Module 11: Using Threads - Notify if any new messages about X are sent
Due Date: 11/07/2021
About this project: The goal of this project is to develop a frontend application that will
interact with the Agent database for a small scale real-world application using third-party
Python libraries (Flask, sqlite3, Crypto.Cipher, Pandas) . In this script, we have the code
for our flask website. The application has added an role based login system and the database
has been encrypted. There is also an option to send an ecrypted message to boss and a database
to keep record of this messages. For the last version an authenticated version of the messaging
server was included. The final feature added to the code was a notification script for different
threads.
Assumptions: N/A
All work below was performed by Luciano Zavala
"""

import string, base64

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

