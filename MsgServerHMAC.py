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


import socketserver
import sqlite3 as sql
import Encryption
import hmac
import hashlib
import random

##################################
#      Boss Server class         #
# Taken from the lectures of the #
#    class made by Dr. Works     #
##################################


class BossServer(socketserver.BaseRequestHandler):

    def handle(self):

        # Handles the data initially
        self.data = self.request.recv(1024).strip()
        hmac_msg = self.data[:len(self.data) - 64]

        # Description
        check_msg = bytes(Encryption.cipher.decrypt(hmac_msg), encoding='utf-8')
        check_tag = self.data[-64:]

        # Validates the authentication key and hash
        if checkAuth(check_msg, check_tag):
            check_msg = check_msg.decode('utf-8')
            check_msg = check_msg.split(maxsplit=1)
            data_one = str(check_msg[0])

            # DataTwo is the Message from the data we receive
            data_two = str(check_msg[1])
            print("{} sent message:".format(data_one))
            print(data_two)

            msg_id = random.randint(1, 100)
            # We connect to our database in order to add the values into the Messages table
            with sql.connect('sqlite3.db') as conn:
                cur = conn.cursor()

                # Execute method to insert the values into the table/database
                cur.execute(
                    "INSERT INTO bossMessage(MessageId, AgentId, Message) VALUES (?, ?, ?)",
                    (msg_id, data_one, data_two))

                # We commit our changes
                conn.commit()

        else:
            print("Unauthenticated message received! Be on alert! Watch out for bad guys!!!")


#####################################
#   check authentication function   #
#####################################

def checkAuth(input_message, message_tag):
    secret = b'1234'

    # Digests the hash code
    hash_code = hmac.new(secret, input_message, digestmod=hashlib.sha3_512).digest()
    if message_tag != hash_code:
        return False
    else:
        return True


if __name__ == '__main__':
    try:
        HOST, PORT = "localhost", 8888
        server = socketserver.TCPServer((HOST, PORT), BossServer)
        server.serve_forever()
    except:
        exit(1)
    finally:
        # We close the server
        server.server_close()
