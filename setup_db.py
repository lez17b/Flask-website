"""
Name: Luciano Zavala
Date: 10/10/2021
Assignment: Module 6: Send Encrypted Message to Boss
Due Date: 10/10/2021
About this project: The goal of this project is to develop a frontend application that will
interact with the Agent database for a small scale real-world application using third-party
Python libraries (Flask, sqlite3, Crypto.Cipher, Pandas) . In this script, we have the code
for our flask website. The application has added an role based login system and the database
has been encrypted. There is alos an option to send an ecrypted message to boss and a database
to keep record of this messages.
Assumptions: N/A
All work below was performed by Luciano Zavala
"""

import sqlite3
from sqlite3 import Error
import string
import base64
import Encryption

# Connection to the database
conn = None
try:
    conn = sqlite3.connect("./sqlite3.db")
    print("connected to db sqlite3")
except Error as e:
    print(e)

# cursor
cursor = conn.cursor()

# Drop statement if table exists
conn.execute('''DROP TABLE secretMessage''')

# Drop statement if table exists
conn.execute('''DROP TABLE bossMessage''')

# Create table statement
cursor.execute(""" CREATE TABLE IF NOT EXISTS secretMessage (
                                        AgentId int PRIMARY KEY, 
                                        AgentName text,
                                        AgentAlias text,
                                        AgentSecurityLevel text,
                                        LoginPassword text
                    )""")

cursor.execute(""" CREATE TABLE IF NOT EXISTS bossMessage(
                                        MessageId int PRIMARY KEY,
                                        AgentId int,   
                                        Message text
                                        )""")

# save changes
conn.commit()
print('Tables created.')

# encryption of user name and password:
nm = str(Encryption.cipher.encrypt(b'Luciano Zavala') .decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'password').decode("utf-8"))
alias = str(Encryption.cipher.encrypt(b'luczze').decode("utf-8"))
# Adding data to the table:
# 1
cursor.execute("""INSERT INTO secretMessage(AgentId, AgentName, AgentAlias, AgentSecurityLevel, LoginPassword)
                    VALUES(?,?,?,?,?);""", (1, nm, alias, '1', pwd))

# 3
nm2 = str(Encryption.cipher.encrypt(b'Anakin Skywalker') .decode("utf-8"))
pwd2 = str(Encryption.cipher.encrypt(b'password').decode("utf-8"))
alias2 = str(Encryption.cipher.encrypt(b'anakin').decode("utf-8"))
cursor.execute("""INSERT INTO secretMessage(AgentId, AgentName, AgentAlias, AgentSecurityLevel, LoginPassword)
                    VALUES(?,?,?,?,?);""", (3, nm2, alias2, '2', pwd2))

# 4
nm3 = str(Encryption.cipher.encrypt(b'Steve Wozniak') .decode("utf-8"))
pwd3 = str(Encryption.cipher.encrypt(b'password').decode("utf-8"))
alias3 = str(Encryption.cipher.encrypt(b'apple').decode("utf-8"))
cursor.execute("""INSERT INTO secretMessage(AgentId, AgentName, AgentAlias, AgentSecurityLevel, LoginPassword)
                    VALUES(?,?,?,?,?);""", (4, nm3, alias3, '2', pwd3))

# 5
nm4 = str(Encryption.cipher.encrypt(b'Yuval Noah') .decode("utf-8"))
pwd4 = str(Encryption.cipher.encrypt(b'password').decode("utf-8"))
alias4 = str(Encryption.cipher.encrypt(b'sapien').decode("utf-8"))
cursor.execute("""INSERT INTO secretMessage(AgentId, AgentName, AgentAlias, AgentSecurityLevel, LoginPassword)
                    VALUES(?,?,?,?,?);""", (5, nm4, alias4, '2', pwd4))

# 6
nm5 = str(Encryption.cipher.encrypt(b'Jeff Bezos') .decode("utf-8"))
pwd5 = str(Encryption.cipher.encrypt(b'password').decode("utf-8"))
alias5 = str(Encryption.cipher.encrypt(b'amazonian').decode("utf-8"))
cursor.execute("""INSERT INTO secretMessage(AgentId, AgentName, AgentAlias, AgentSecurityLevel, LoginPassword)
                    VALUES(?,?,?,?,?);""", (6, nm5, alias5, '2', pwd5))

#       MESSAGE TABLE
cursor.execute("""INSERT INTO bossMessage(MessageId, AgentId, Message)VALUES(1, 1, 'test message 1' );""")

cursor.execute("""INSERT INTO bossMessage(MessageId, AgentId, Message)VALUES(2, 1, 'test message 2' );""")

cursor.execute("""INSERT INTO bossMessage(MessageId, AgentId, Message)VALUES(3, 1, 'test message 3' );""")

cursor.execute("""INSERT INTO bossMessage(MessageId, AgentId, Message)VALUES(4, 1, 'test message 4' );""")

cursor.execute("""INSERT INTO bossMessage(MessageId, AgentId, Message)VALUES(5, 1, 'test message 5' );""")

cursor.execute("""INSERT INTO bossMessage(MessageId, AgentId, Message)VALUES(6, 1, 'test message 6' );""")


# Commit changes
conn.commit()
print("connection committed")

# Connection closed
conn.close()
print("Connection closed")