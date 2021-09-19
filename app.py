from flask import Flask, render_template

app = Flask(__name__)


# Index page
@app.route('/')
def index():
    return render_template('home.html')


# List page
@app.route('/list')
def list_records():
    return render_template('list.html')


# Add new secret agent page
@app.route('/enternew')
def enter_new_agent():
    return render_template('enternew.html')


# error in the query landing page
@app.route('/addrec')
def wrong_query():
    return 'wrong query'


if __name__ == '__main__':
    app.run(debug=True)
