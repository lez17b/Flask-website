"""
Name: Luciano Zavala
Date: 11/07/2021
Assignment: Module 11: Using Threads - Notify if any new messages about X are sent
Due Date: 11/07/2021
About this project: The goal of this project is to develop a frontend application that will
interact with the Agent database for a small scale real-world application using third-party
Python libraries (Flask, sqlite3, Crypto.Cipher, Pandas) . In this script, we have the code
for our flask website. The application has added an role based login system and the database
has been encrypted. There is also an option to send an encrypted message to boss and a database
to keep record of this messages. For the last version an authenticated version of the messaging
server was included. The final feature added to the code was a notification script for different
threads.
Assumptions: N/A
All work below was performed by Luciano Zavala
"""

from concurrent.futures import ThreadPoolExecutor
import sqlite3 as sql

##################################
#   Notifications using threads  #
# Taken from the lectures of the #
#    class made by Dr. Works     #
##################################


# Find the string function
def findString(x):
    num_of_string = 0
    # connect to the db
    with sql.connect('sqlite3.db') as conn:
        conn.row_factory = sql.Row
        cur = conn.cursor()

        # Selection query
        sql_select_query = """SELECT COUNT(*) as numberOfMSG from bossMessage where Message like ? """
        cur.execute(sql_select_query, ("%" + x + "%",))

        row = cur.fetchone()
        num_of_string = int(row[0])
    conn.close()
    return num_of_string


def main():
    # Initialization strings
    first_string = "hello"
    second_string = "world"
    num_of_hello_msg = findString(first_string)
    num_of_world_msg = findString(second_string)

    # Loop continuously
    while True:
        with ThreadPoolExecutor(max_workers=2) as e:
            task_num_find_hello = e.submit(findString, first_string)
            task_num_find_world = e.submit(findString, second_string)

        if task_num_find_hello.result() != num_of_hello_msg:
            num_of_hello_msg = task_num_find_hello.result()
            print(f'Now there are {str(num_of_hello_msg)} messages about {first_string}')

        if task_num_find_world.result() != num_of_world_msg:
            num_of_world_msg = task_num_find_world.result()
            print(f'Now there are {str(num_of_world_msg)} messages about {second_string}')


if __name__ == '__main__':
    main()

