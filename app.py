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
        try:
            agent_nm = request.form['AgentName']
            agent_alias = request.form['AgentAlias']
            agent_security_lvl = request.form['AgentSecurityLvl']
            login_password = request.form['LoginPassword']

            with sql.connect("sqlite3.db") as con:
                cur = con.cursor()
                cur.execute(" INSERT INTO secretMessage (AgentId,AgentName,AgentAlias,LoginPassword) VALUES(?, ?, ?, ?) ",
                            (agent_nm, agent_alias, agent_security_lvl, login_password))

                con.commit()
                msg = "Record successfully added"
        except:
            con.rollback()
            msg = "You cannot enter an empty name\n\tYou cannot enter in an empty alias\n" \
                  "The security level must be a numeric value from 1 to 10\nYou cannot enter an empty password"

        finally:
            return render_template("addrec.html", msg=msg)
            con.close()


if __name__ == '__main__':
    app.run(debug=True)
