from flask import Flask, render_template
from TicketSystem import app
import sqlite3

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

def get_db_connection():
    conn = sqlite3.connect('ticketdb.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
@app.route("/home")
def home():
    """Renders a welcome page."""
    return render_template("homepage.html")

@app.route("/login")
def login():
    """Renders a log in page"""
    conn = get_db_connection()
    users = conn.execute('SELECT * FROM USERS').fetchall()
    conn.close()
    return render_template("login.html", users=users)

@app.route("/dashboard")
def dashboard():
    """Renders a log in page"""
    return render_template("dashboard.html")

@app.route("/activetickets")
def activetickets():
    """Renders a log in page"""
    conn = get_db_connection()
    #EDIT THIS TO ONLY LOAD THOSE WITH NOT A 'DONE' STATUS
    tickets = conn.execute('SELECT * FROM Tickets').fetchall()
    conn.close()
    return render_template("activetickets.html", tickets=tickets)

@app.route("/completedtickets")
def completedtickets():
    """Renders a log in page"""
    return render_template("completedtickets.html")

@app.route("/newticket")
def newticket():
    """Renders a log in page"""
    return render_template("newticket.html")

if __name__ == "__main__":
    app.run()
