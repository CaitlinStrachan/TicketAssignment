from flask import Flask, render_template,request,redirect,url_for,flash
from TicketSystem import app
import sqlite3 as sql


# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqllite:///ticket.db'

#initialise the database
#db = SQLAlchemy(app)

#create db model 


def get_db_connection():
    conn = sql.connect('ticketdb.db')
    conn.row_factory = sql.Row
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
    return render_template("dashboard.html")

@app.route("/activetickets")
def activetickets():
    conn = get_db_connection()
    cursor = conn.cursor()
    #ONLY LOAD THOSE WITH NOT A 'DONE' STATUS
    cursor.execute('SELECT * FROM Tickets WHERE Status NOT LIKE "Done"')
    tickets = cursor.fetchall()
    return render_template("activetickets.html", tickets=tickets)

@app.route("/activetickets/edit/<string:TicketID>", methods=['POST','GET'])
def editactivetickets(TicketID):
    if request.method=='POST':
        Description=request.form['Description']
        ProductName=request.form['ProductName']
        TeamID=request.form['TeamID']
        ClientBackup=request.form['ClientBackup']
        Priority=request.form['Priortiy']
        Status=request.form['Status']
        #DateRaised=request.form['DateRaised']
        DateResolved=request.form['DateResolved']       
        conn = get_db_connection()
        cursor=conn.cursor()
        cursor.execute("UPDATE Tickets SET Description=?,ProductName=?,TeamID=?,ClientBackup=?,Priority=?,Status=?,DateResolved=? WHERE TicketID=?", (Description,ProductName,TeamID,ClientBackup,Priority,Status,DateResolved,TicketID))
        conn.commit()
        #flash('User Updated','success')
        return redirect(url_for("activetickets"))
    conn = get_db_connection()
    conn.row_factory=sql.Row
    cursor = conn.cursor()
    #ONLY LOAD THE SELECTED TICKET TO EDIT
    cursor.execute('SELECT * FROM Tickets WHERE TicketID=?', TicketID)
    tickets = cursor.fetchone()
    return render_template("editactivetickets.html", tickets=tickets)

@app.route("/completedtickets")
def completedtickets():
    """Renders a log in page"""
    conn = get_db_connection()
    cursor = conn.cursor()
    #ONLY LOAD THOSE WITH A 'DONE' STATUS
    cursor.execute('SELECT * FROM Tickets WHERE Status = "Done"')
    tickets = cursor.fetchall()
    return render_template("completedtickets.html", tickets=tickets)

@app.route("/newticket", methods=['POST','GET'])
def newticket():
    if request.method=='POST':
        Description=request.form['Description']
        ProductName=request.form['ProductName']
        TeamID=request.form['TeamID']
        ClientBackup=request.form['ClientBackup']
        Priority=request.form['Priortiy']
        Status=request.form['Status']
        DateRaised=request.form['DateRaised']
        #DateResolved=request.form['DateResolved']       
        conn = get_db_connection()
        cursor=conn.cursor()
        cursor.execute("INSERT into Tickets (Description,ProductName,TeamID,ClientBackup,Priority,Status,DateRaised) values (?,?,?,?,?,?,?)",(Description,ProductName,TeamID,ClientBackup,Priority,Status,DateRaised))
        conn.commit()
        #flash('Ticket Updated','success')
        return redirect(url_for("dashboard"))   
    return render_template("newticket.html")

@app.route("/deleteticket/<string:TicketID>",methods=['GET'])
def deleteticket(TicketID):
    conn = get_db_connection()
    cursor=conn.cursor()
    cursor.execute("delete from Tickets where TicketID=?",(TicketID,))
    conn.commit()
    #flash('Ticket Deleted','warning')
    return redirect(url_for("activetickets"))


if __name__ == "__main__":
    app.run()
