from flask import Flask, render_template
from TicketSystem import app
import sqlite3
import flask_sq

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
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM USERS')
    users = cursor.fetchall()
    return render_template("login.html", users=users)

@app.route("/dashboard")
def dashboard():
    """Renders a log in page"""
    return render_template("dashboard.html")

@app.route("/activetickets")
def activetickets():
    """Renders a log in page"""
    conn = get_db_connection()
    cursor = conn.cursor()
    #ONLY LOAD THOSE WITH NOT A 'DONE' STATUS
    cursor.execute('SELECT * FROM Tickets WHERE Status NOT LIKE "Done"')
    tickets = cursor.fetchall()
    return render_template("activetickets.html", tickets=tickets)

@app.route("/activetickets/edit")
def editactivetickets():
    conn = get_db_connection()
    cursor = conn.cursor()
    #ONLY LOAD THOSE WITH NOT A 'DONE' STATUS
    cursor.execute('SELECT * FROM Tickets WHERE Status NOT LIKE "Done"')
    tickets = cursor.fetchall()
    return render_template("editactivetickets.html", tickets=tickets)

@app.route("/completedtickets")
def completedtickets():
    """Renders a log in page"""
    conn = get_db_connection()
    cursor = conn.cursor()
    #ONLY LOAD THOSE WITH A 'DONE' STATUS
    cursor.execute('SELECT * FROM Tickets WHERE Status = "Done"')
    tickets = cursor.fetchall()
    """Renders a log in page"""
    return render_template("completedtickets.html", tickets=tickets)

@app.route("/newticket")
def newticket():
    """Renders a log in page"""
    return render_template("newticket.html")

if __name__ == "__main__":
    app.run()
