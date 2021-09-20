from flask import Flask, render_template, request
import sqlite3 as sql
from sqlite3 import Error

app = Flask(__name__)


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

        agent_nm = str(request.form['AgentName'])
        agent_alias = str(request.form['AgentAlias'])
        agent_security_lvl = request.form['AgentSecurityLvl']
        login_password = str(request.form['LoginPassword'])
        try:
            if not agent_nm or agent_nm.isspace() or not agent_alias or agent_alias.isspace() \
                    or not login_password or login_password.isspace():
                raise Exception

            with sql.connect("sqlite3.db") as con:
                cur = con.cursor()
                cur.execute(" INSERT INTO secretMessage (AgentName,AgentAlias,AgentSecurityLvl,LoginPassword) VALUES(?, ?, ?, ?) ",
                            (agent_nm, agent_alias, agent_security_lvl, login_password))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "Error(s) in insert operation: "
            if not agent_nm or agent_nm.isspace():
                msg += "\nName cannot be empty."
            if not agent_alias or agent_alias.isspace():
                msg += "\nAlias cannot be empty."
            if not login_password or login_password.isspace():
                msg += "\nPassword cannot be empty."
        finally:
            msg = msg.split('\n')
            return render_template("addrec.html", msg=msg)
            con.close()


if __name__ == '__main__':
    app.run(debug=True)
