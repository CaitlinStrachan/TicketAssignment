from flask import Flask, render_template
from TicketSystem import app

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route("/")
@app.route("/home")
def home():
    """Renders a welcome page."""
    return render_template("homepage.html")

@app.route("/login")
def login():
    """Renders a log in page"""
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    """Renders a log in page"""
    return render_template("dashboard.html")

@app.route("/activetickets")
def activetickets():
    """Renders a log in page"""
    return render_template("activetickets.html")

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
