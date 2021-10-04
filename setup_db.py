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

# Create table statement
cursor.execute(""" CREATE TABLE IF NOT EXISTS secretMessage (
                                        AgentId int PRIMARY KEY, 
                                        AgentName text,
                                        AgentAlias text,
                                        AgentSecurityLevel text,
                                        LoginPassword text
                    )""")

# save changes
conn.commit()
print('Player Table created.')

# encryption of user name and password:
nm = str(Encryption.cipher.encrypt(b'Luciano Zavala') .decode("utf-8"))
pwd = str(Encryption.cipher.encrypt(b'password').decode("utf-8"))

# Adding data to the table:
# 1
cursor.execute("""INSERT INTO secretMessage(AgentId, AgentName, AgentAlias, AgentSecurityLevel, LoginPassword)
                    VALUES(?,?,?,?,?);""", (1, nm, 'luczze', '1', pwd))

# testing record
cursor.execute("""INSERT INTO secretMessage(AgentId, AgentName, AgentAlias, AgentSecurityLevel, LoginPassword)
                    VALUES(?,?,?,?,?);""", (2, 'Luciano Zavala', 'luczze', '1', 'password'))

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
# Commit changes
conn.commit()
print("connection committed")

# Connection closed
conn.close()
print("Connection closed")