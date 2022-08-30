from functools import wraps
#from winreg import REG_NOTIFY_CHANGE_ATTRIBUTES
from flask import Flask,render_template,request,redirect,session,url_for,flash
#from flask_wtf import FlaskForm
from TicketSystem import app
import sqlite3 as sql
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
import os
#from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
#from wtforms import StringField, SubmitField
#from wtforms.validators import DataRequired 
import hashlib
import secrets
#from forms import LoginForm

#set secret key 
secretkey = os.urandom(12).hex()

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'ticketdb'
app.config['SECRET_KEY'] = secretkey

# Intialize MySQL
mysql = MySQL(app)

def get_db_connection():
    conn = sql.connect('ticketdb.db')
    conn.row_factory = sql.Row
    return conn

@app.route("/")
@app.route("/home")
def home():
    """Renders a welcome page."""
    return render_template("homepage.html")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Create variables for easy access
        email = request.form['email']
        password = request.form['password']
        #check account exists
        conn = get_db_connection()
        #cursor = mysql.connection.cursor()
        cursor = conn.cursor()
        #check the password using the hash value of the entered password
        cursor.execute("SELECT * FROM USERS WHERE Email=? AND Password=?", (email, hashlib.md5(password.encode()).hexdigest(),))
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = secrets.token_urlsafe(16)
            session['email'] = account['email']
            session['adminLevel'] = account['AdminLevel']
            # Redirect to home page
            flash('Logged in Successfully','success')
            return redirect('dashboard')
        else:
            # Account doesnt exist or username/password incorrect
            flash('Incorrect username/password!','danger')
    return render_template("login.html")

#check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('login'))
	return wrap


@app.route("/dashboard")
def dashboard():
     # Check if user is loggedin
    if 'loggedin' in session:
        #check if user is admin 
        adminLevel = session['adminLevel']
        if 'Admin' in adminLevel:          
       # User is loggedin show them the home page
            return render_template("adminDashboard.html")
        else: 
            return render_template("dashboard.html")
        
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/activetickets")
def activetickets():
    conn = get_db_connection()
    cursor = conn.cursor()
    #ONLY LOAD THOSE WITH NOT A 'DONE' STATUS
    cursor.execute('SELECT * FROM Tickets WHERE Status NOT LIKE "Done"')
    tickets = cursor.fetchall()
    if 'loggedin' in session:
        #check if user is admin 
        adminLevel = session['adminLevel']
        if 'Admin' in adminLevel:          
           # User is loggedin show them the home page
           return render_template("activetickets.html", tickets=tickets)
        else: 
           return render_template("activeticketsUser.html", tickets=tickets)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/activetickets/edit/<string:TicketID>", methods=['POST','GET'])
def editactivetickets(TicketID):
    if request.method=='POST':
        #remove stray } from ticket ID 
        TicketID = TicketID.rstrip('}')
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
        conn.close()
        flash('Ticket Updated Successfully','success')
        return redirect(url_for("activetickets"))
    conn = get_db_connection()
    conn.row_factory=sql.Row
    cursor = conn.cursor()
    #ONLY LOAD THE SELECTED TICKET TO EDIT
    cursor.execute('SELECT * FROM Tickets WHERE TicketID=?', [TicketID])
    tickets = cursor.fetchone()
    if 'loggedin' in session:
        #check if user is admin 
        adminLevel = session['adminLevel']
        if 'Admin' in adminLevel:          
           # User is loggedin show them the home page
           return render_template("editactivetickets.html", tickets=tickets)
        else: 
           return render_template("notAdminErrorPage.html", tickets=tickets)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/completedtickets")
def completedtickets():
    """Renders a log in page"""
    conn = get_db_connection()
    cursor = conn.cursor()
    #ONLY LOAD THOSE WITH A 'DONE' STATUS
    cursor.execute('SELECT * FROM Tickets WHERE Status = "Done"')
    tickets = cursor.fetchall()
    if 'loggedin' in session:
        return render_template("completedtickets.html", tickets=tickets)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

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
        conn.close()
        flash('Ticket Added Successfully','success')
        return redirect(url_for("dashboard"))
    if 'loggedin' in session:
        return render_template("newticket.html")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/deleteticket/<string:TicketID>",methods=['GET'])
def deleteticket(TicketID):    
    if 'loggedin' in session:
        conn = get_db_connection()
        cursor=conn.cursor()
        cursor.execute("delete from Tickets where TicketID=?",(TicketID,))
        conn.commit()
        conn.close()    
        flash('Ticket Deleted Sucesffully','warning')
        return redirect(url_for("activetickets"))
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/users")
def users():
    conn = get_db_connection()
    cursor = conn.cursor()
    #Load all users
    cursor.execute('SELECT * FROM USERS')
    users = cursor.fetchall()
    #check if user is admin 
    adminLevel = session['adminLevel']
    if 'loggedin' in session:
        if 'Admin' in adminLevel:          
           # User is loggedin show them the home page
           return render_template("users.html", users=users)
        else: 
           return render_template("notAdminErrorPage.html")
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route("/newuser", methods=['POST','GET'])
def newuser():
    if request.method=='POST':
        Username=request.form['Username']
        Email=request.form['Email']
        #get the password 
        plainPass=request.form['Password']
        #save the password as a hash 
        md5 = hashlib.md5(plainPass.encode())
        #save the password in hex value to allow for saving to the database
        Password = md5.hexdigest()
        AdminLevel=request.form['AdminLevel']       
        conn = get_db_connection()
        cursor=conn.cursor()
        cursor.execute("INSERT into USERS (Username,Email,Password,AdminLevel) values (?,?,?,?)",(Username,Email,Password,AdminLevel))
        conn.commit()
        conn.close()
        flash('User Added','success')
        return redirect(url_for("users"))
    adminLevel = session['adminLevel']
    if 'loggedin' in session:
        if 'Admin' in adminLevel:          
           # User is loggedin as admin show them the new user page
           return render_template("newuser.html")
        else: 
           return render_template("notAdminErrorPage.html")  
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

#logout
@app.route("/logout")
def logout():
	session.clear()
	#flash('You are now logged out','success')
	return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
