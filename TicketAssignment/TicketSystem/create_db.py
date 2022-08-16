import sqlite3 as sql

#connect to SQLite
conn = sql.connect('ticketdb.db')

cur = conn.cursor()

#Delete tables if already exist
cur.execute("DROP TABLE USERS")

cur.execute('''CREATE TABLE USERS
         (UserID INT PRIMARY KEY     NOT NULL,
          Username           TEXT    NOT NULL,
          Email              VARCHAR(50)    NOT NULL,
          Password           VARCHAR(50)    NOT NULL,
          AdminLevel         TEXT    NOT NULL);''')
print ("Users Table created successfully");

cur.execute("DROP TABLE TEAMS")
cur.execute('''CREATE TABLE TEAMS
         (TeamID INT PRIMARY KEY        NOT NULL,
          TeamName              TEXT    NOT NULL,
          PrimaryContactName    TEXT    NOT NULL,
          PrimaryContactEmail   VARCHAR(50)    NOT NULL,
          SecondaryContactName  TEXT    NOT NULL,
          SecondaryContactEmail VARCHAR(50)    NOT NULL);''')
print ("Teams table created successfully");

cur.execute("DROP TABLE Products")

cur.execute('''CREATE TABLE Products
         (ProductID INT PRIMARY KEY     NOT NULL,
          ProductName         TEXT      NOT NULL,
          ProductType         TEXT      NOT NULL,
          TeamID              INT       NOT NULL);''')
print ("Products table created successfully");

cur.execute("DROP TABLE Tickets")

cur.execute('''CREATE TABLE Tickets
         (TicketID INT PRIMARY KEY         NOT NULL,
          Description        TEXT          NOT NULL,
          ClientBackup       VARCHAR(50),
          Priority           VARCHAR(2)    NOT NULL,
          Status             TEXT          NOT NULL,
          DateRaised         TEXT          NOT NULL,
          DateResolved       TEXT,
          ProductName        TEXT          NOT NULL,
          TeamID             INT           NOT NULL);''')
print ("Tickets table created successfully");

#commit changes
cur.commit()

#close the connection
cur.close()
