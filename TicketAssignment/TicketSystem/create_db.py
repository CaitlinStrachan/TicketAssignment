import sqlite3 as sql

#connect to SQLite
conn = sql.connect('ticketdb.db')

cur = conn.cursor()

#Delete tables if already exist
cur.execute("DROP TABLE IF EXISTS USERS")

cur.execute('''CREATE TABLE USERS
         (UserID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
          Username           TEXT    NOT NULL,
          Email              VARCHAR(50)    NOT NULL,
          Password           VARCHAR(50)    NOT NULL,
          AdminLevel         TEXT    NOT NULL);''')
print ("Users Table created successfully");

cur.execute("DROP TABLE IF EXISTS TEAMS")
cur.execute('''CREATE TABLE TEAMS
         (TeamID INTEGER PRIMARY KEY AUTOINCREMENT,
          TeamName              TEXT    NOT NULL,
          PrimaryContactName    TEXT    NOT NULL,
          PrimaryContactEmail   VARCHAR(50)    NOT NULL,
          SecondaryContactName  TEXT    NOT NULL,
          SecondaryContactEmail VARCHAR(50)    NOT NULL);''')
print ("Teams table created successfully");

cur.execute("DROP TABLE IF EXISTS Products")

cur.execute('''CREATE TABLE Products
         (ProductID INTEGER PRIMARY KEY AUTOINCREMENT,
          ProductName         TEXT      NOT NULL,
          ProductType         TEXT      NOT NULL,
          TeamID              INT       NOT NULL);''')
print ("Products table created successfully");

cur.execute("DROP TABLE IF EXISTS Tickets")

cur.execute('''CREATE TABLE Tickets
         (TicketID INTEGER PRIMARY KEY AUTOINCREMENT,
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
conn.commit()

#close the connection
conn.close()
