"""
Name: Luciano Zavala
Date: 09/15/2021
Assignment: Module 4: Basic Flask Website
Due Date: 01/31/2021
About this project: The goal of this project is to develop a frontend application that will
interact with the SecretAgent database for a small scale real-world application using third-party
Python libraries. In this script, we have the code for our flask website.
Assumptions: N/A
All work below was performed by Luciano Zavala
"""

from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)
app.debug = True

# Index page
@app.route('/')
def index():
    return render_template('home.html')


# List page
@app.route('/list')
def list_records():
    con = sql.connect("sqlite3.db")
    con.row_factory = sql.Row

    cur = con.cursor()
    cur.execute("select * from secretMessage")

    rows = cur.fetchall()
    return render_template("list.html", rows=rows)


# Add new secret agent page
@app.route('/enternew')
def enter_new_agent():
    return render_template('enternew.html')


# Add record route
@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
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
                message += "Error! The SecurityLevel must be an integer.\n"
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

            # Inside this if statement, we connect to our database
            if not err:
                with sql.connect('sqlite3.db') as conn:
                    cur = conn.cursor()

                    # Execute method to insert the values into the table/database
                    cur.execute(
                        "INSERT INTO SecretAgent(AgentName,AgentAlias,AgentSecurityLevel,LoginPassword) VALUES (?,?,?,?)",
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


if __name__ == '__main__':
    app.run(debug=True)
