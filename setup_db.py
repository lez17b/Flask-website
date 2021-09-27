import sqlite3
from sqlite3 import Error

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
                                        AgentName text PRIMARY KEY,
                                        AgentAlias text,
                                        AgentSecurityLevel text,
                                        LoginPassword text
                    )""")

# Adding data to the table:

# 1
cursor.execute("""INSERT INTO secretMessage(AgentName, AgentAlias, AgentSecurityLevel, LoginPassword)
                    VALUES ('Luciano Zavala', 'luczze', '1', 'password');""")

# Commit changes
conn.commit()
print("connection committed")

# Connection closed
conn.close()
print("Connection closed")