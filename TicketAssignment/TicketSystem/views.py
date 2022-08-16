from flask import Flask
from TicketSystem import app

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app


@app.route("/")
@app.route("/home")
def home():
    """Renders a sample page."""
    return "Homepage"

@app.route("/login")
def login():
    """Renders a sample page."""
    return "Login"

if __name__ == "__main__":
    app.run()
