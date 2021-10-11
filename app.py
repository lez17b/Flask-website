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

import os
from flask import Flask, render_template, request, session, flash
import sqlite3 as sql
import Encryption
import pandas as pd
import socket
import random

app = Flask(__name__)
app.debug = True


# Index page
@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html', name=session['name'], security=session['admin'])


# Help page
@app.route('/help')
def help():
    if not session.get('logged_in'):
        return render_template('help.html')
    else:
        return render_template('help.html', name=session['name'])


# Send help posting method
@app.route('/help', methods=['POST'])
def send_help_message():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':
            try:
                err = False  # Error assigned to false for error checking
                message = ""  # Message we will print out using the addrec.html page
                agent_id = str(session.get('agentId'))
                msg = request.form['message']

                # Concatenate the message and id
                msg = agent_id + ";" + msg

                if not msg or msg.isspace():
                    message += "Error! The Message field cannot be empty.\n"
                    err = True  # Assign true to the error variable

                # Encrypt message
                msg = str(Encryption.cipher.encrypt(bytes(msg, 'utf-8')).decode('utf-8'))

                HOST, PORT = "localhost", 9999
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                # Connect to server and send data
                sock.connect((HOST, PORT))

                sock.sendall(bytes(msg, "utf-8"))

                sock.close()

                message += "Help message sent!"
            except sock.error as e:
                message += "Error sending help message:", e
            finally:
                msg_id = random.randint(1, 100)
                if not err:
                    with sql.connect('./sqlite3.db') as conn:
                        cur = conn.cursor()

                        # Execute method to insert the values into the table/database
                        cur.execute("""INSERT INTO bossMessage(MessageId, AgentId, Message)VALUES(?, ?, ?);""",
                                    (msg_id, agent_id, msg))
                        # We commit our changes
                        conn.commit()
                # message += "Record added successfully!"
                return render_template("addrec.html", msg=str(message))


# List page
@app.route('/list')
def list_records():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        con = sql.connect("sqlite3.db")
        con.row_factory = sql.Row

        cur = con.cursor()
        cur.execute("select * from secretMessage")
        rows = cur.fetchall()

        # data frame creation
        df = pd.DataFrame(rows, columns=['AgentId', 'AgentName', 'AgentAlias', 'AgentSecurityLevel', 'LoginPassword'])

        # The code is based on the class given by Dr. works and also the implementation from module 6 videos
        # CODE BLOCK: convert to an array

        # Agent Name decryption
        i = 0
        for name in df['AgentName']:
            nm = str(Encryption.cipher.decrypt(name))
            df._set_value(i, 'AgentName', nm)
            i += 1

        # Agent Alias decryption
        ii = 0

        for alias in df['AgentAlias']:
            alias = str(Encryption.cipher.decrypt(alias))
            df._set_value(ii, 'AgentAlias', alias)
            ii += 1

        con.close()
        # print(df)
        return render_template("list.html", rows=df)


# Add new secret agent page
@app.route('/enternew')
def enter_new_agent():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('enternew.html')


# Add record route
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        if request.method == 'POST':

            try:
                err = False  # Error assigned to false for error checking
                message = ""  # Message we will print out using the result.html page

                # Assigning name to a variable and validating it
                name = request.form["AgentName"]
                if not name or name.isspace():
                    message += "Error! The Name field cannot be empty.\n"
                    err = True  # Assign true to the error variable
                # Encrypt name value
                crypt_name = str(Encryption.cipher.encrypt(bytes(name, 'utf-8')).decode("utf-8"))

                # Assigning alias to a variable and validating it
                alias = request.form["AgentAlias"]
                if not alias or alias.isspace():
                    message += "Error! The Alias field cannot be empty.\n"
                    err = True
                # Encrypt alias value
                crypt_alias = str(Encryption.cipher.encrypt(bytes(alias, 'utf-8')).decode("utf-8"))

                # Try-Except statement to assign security level to a variable and validate it

                try:
                    security_level = int(request.form["AgentSecurityLevel"])
                except:
                    message += "Error! The Security Level must be an integer.\n"
                    err = True
                else:
                    # If statement to ensure that the security_level value is between 1 and 10
                    if security_level < 1 or security_level > 10:
                        message += "Error! The SecurityLevel must be between the values 1 and 10.\n"
                        err = True

                # Assigning password to a variable and validating it
                password = request.form["LoginPassword"]
                if not password or password.isspace():
                    message += "Error! The Password field cannot be empty.\n"
                    err = True
                # Encrypt Password value
                crypt_password = str(Encryption.cipher.encrypt(bytes(password, 'utf-8')).decode("utf-8"))

                # Inside this if statement, we connect to our database
                if not err:
                    with sql.connect('./sqlite3.db') as conn:
                        print("conected")
                        cur = conn.cursor()

                        # Execute method to insert the values into the table/database
                        cur.execute(
                            "INSERT INTO secretMessage(AgentName,AgentAlias,AgentSecurityLevel,LoginPassword) VALUES (?,?,?,?)",
                            (crypt_name, crypt_alias, security_level, crypt_password))

                        # We commit our changes
                        conn.commit()
                        message = "Record added successfully!"

            # Except statement that will rollback if the record was not added successfully
            except:
                conn.rollback()
                message = "Record was NOT added successfully"
            finally:
                msg = message.split('\n')
                return render_template("addrec.html", msg=msg)
                conn.close()


# Logout route
@app.route("/logout")
def logout():
    session['name'] = ""
    session['logged_in'] = False
    return index()


# Login page and authentication
@app.route('/login', methods=['POST'])
def do_admin_login():
    try:
        # gets the user name and password and the encrypts each one
        name = request.form['AgentName']
        nm = str(Encryption.cipher.encrypt(bytes(name, 'utf-8')).decode("utf-8"))
        pwd = request.form['LoginPassword']
        pwd = str(Encryption.cipher.encrypt(bytes(pwd, 'utf-8')).decode("utf-8"))

        with sql.connect("sqlite3.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

        # call the DB for the records
        sql_select_query = """select * from secretMessage where AgentName = ? and LoginPassword = ?"""
        cur.execute(sql_select_query, (nm, pwd))

        # Definition of the global session variables
        row = cur.fetchone()
        if row is not None:
            session['name'] = str(Encryption.cipher.decrypt(nm))
            session['logged_in'] = True
            session['agentId'] = row['AgentId']

            # Security level assignation
            if int(row['AgentSecurityLevel']) == 1:
                session['admin'] = 1
            elif int(row['AgentSecurityLevel']) == 2:
                session['admin'] = 2
            else:
                session['admin'] = 3

        else:
            session['logged_in'] = False
            flash('invalid username and/or password invalid!')
    except:
        con.rollback()
        flash("error in insert operation")
    finally:
        con.close()
    return index()


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)
