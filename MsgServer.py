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
import Encryption

##################################
#      MyTCPHandler class        #
# Taken from the lectures of the #
#    class made by Dr. Works     #
##################################


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request	is	the	TCP	socket	connected	to	the	client
        self.data = self.request.recv(1024).strip()
        self.data = str(Encryption.cipher.decrypt(self.data))
        data = self.data.split(";")
        id = data[0]
        msg = data[1]
        print("{}	sent message:	".format(id))
        print(msg)


if __name__ == "__main__":
    try:
        HOST, PORT = "localhost", 9999
        # Create	the	server,	binding	to	localhost	on	port	9999
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        # Activate	the	server;	this	will	keep	running	until	you
        # interrupt	the	program	with	Ctrl-C
        server.serve_forever()
    except server.error as e:
        print("Error:", e)
        exit(1)
    finally:
        server.close()
