"""
Name: Luciano Zavala
Date: 09/26/2021
Assignment: Module 5: Role Based Access Control
Due Date: 09/26/2021
About this project: The goal of this project is to develop a frontend application that will
interact with the SecretAgent database for a small scale real-world application using third-party
Python libraries. In this script, we have the code for our flask website. The application has added role based
and a login system.
Assumptions: N/A
All work below was performed by Luciano Zavala
"""

import os
from flask import Flask, render_template, request, session, flash
import sqlite3 as sql


app = Flask(__name__)
app.debug = True


# Index page
@app.route('/')
def index():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('home.html', name=session['name'], security=session['admin'])


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
        return render_template("list.html", rows=rows)


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

                # Assigning alias to a variable and validating it
                alias = request.form["AgentAlias"]
                if not alias or alias.isspace():
                    message += "Error! The Alias field cannot be empty.\n"
                    err = True

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
                        global_security_level = security_level

                # Assigning password to a variable and validating it
                password = request.form["LoginPassword"]
                if not password or password.isspace():
                    message += "Error! The Password field cannot be empty.\n"
                    err = True

                # Inside this if statement, we connect to our database
                if not err:
                    with sql.connect('./sqlite3.db') as conn:
                        print("conected")
                        cur = conn.cursor()

                        # Execute method to insert the values into the table/database
                        cur.execute(
                            "INSERT INTO secretMessage(AgentName,AgentAlias,AgentSecurityLevel,LoginPassword) VALUES (?,?,?,?)",
                            (name, alias, security_level, password))

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


@app.route("/logout")
def logout():
    session['name'] = ""
    session['logged_in'] = False
    return index()


@app.route('/login', methods=['POST'])
def do_admin_login():
    try:
        nm = request.form['AgentName']
        pwd = request.form['LoginPassword']

        with sql.connect("sqlite3.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

        sql_select_query = """select * from secretMessage where AgentName = ? and LoginPassword = ?"""
        cur.execute(sql_select_query, (nm, pwd))

        row = cur.fetchone()
        if row is not None:
            session['name'] = nm
            session['logged_in'] = True

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

