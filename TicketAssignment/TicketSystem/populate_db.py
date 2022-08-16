import sqlite3 as sql

#connect to SQLite
conn = sql.connect('ticketdb.db')

conn.execute('''INSERT INTO USERS (UserID, Username, Email, Password, AdminLevel)
             VALUES (1, 'Admin1', 'admin1@gmail.com', '4dm!n', 'Admin');''')
conn.execute('''INSERT INTO USERS (UserID, Username, Email, Password, AdminLevel)
             VALUES (2, 'User1', 'user1@gmail.com', 'u$erP4$$', 'User');''')
print ("Users added successfully");

conn.execute('''INSERT INTO TEAMS (TeamID, TeamName, PrimaryContactName, PrimaryContactEmail, SecondaryContactName, SecondaryContactEmail)
             VALUES (1, 'ApTax', 'Sue Brownhill', 'sue.b@gmail.com', 'Caitlin Strachan', 'caitlin.s@gmail.com');''')
conn.execute('''INSERT INTO TEAMS (TeamID, TeamName, PrimaryContactName, PrimaryContactEmail, SecondaryContactName, SecondaryContactEmail)
             VALUES (2, 'Delta', 'Carl Jacko', 'carl.j@gmail.com', 'Lyle Davidson', 'lyle.d@gmail.com');''')
conn.execute('''INSERT INTO TEAMS (TeamID, TeamName, PrimaryContactName, PrimaryContactEmail, SecondaryContactName, SecondaryContactEmail)
             VALUES (3, 'Tax Desktop', 'Mark Cleggo', 'mark.k@gmail.com', 'Gareth Hoole', 'gareth.h@gmail.com');''')
print ("Teams added successfully");

conn.execute('''INSERT INTO Products (ProductID, ProductName, ProductType, TeamID)
             VALUES (1, 'Accounts Production Online', 'Online', 1);''')
conn.execute('''INSERT INTO Products (ProductID, ProductName, ProductType, TeamID)
             VALUES (2, 'Corporation Tax Online', 'Online', 1);''')
conn.execute('''INSERT INTO Products (ProductID, ProductName, ProductType, TeamID)
             VALUES (3, 'Accounts Production Advanced', 'Desktop', 1);''')
conn.execute('''INSERT INTO Products (ProductID, ProductName, ProductType, TeamID)
             VALUES (4, 'Client Management', 'Online', 2);''')
conn.execute('''INSERT INTO Products (ProductID, ProductName, ProductType, TeamID)
             VALUES (5, 'Tax Desktop', 'Desktop', 3);''')
print ("Products added successfully");


conn.execute('''INSERT INTO Tickets (TicketID, Description, ClientBackup, Priority, Status, DateRaised, DateResolved, ProductName, TeamID)
             VALUES (1, 'Crash on launch to SAT', 'z:\AP\Escalations\ClientBackup\GHB001', 'P1', 'In Progess', '01/08/2022', NULL, 'Accounts Production Advanced', 1);''')
conn.execute('''INSERT INTO Tickets (TicketID, Description, ClientBackup, Priority, Status, DateRaised, DateResolved, ProductName, TeamID)
             VALUES (2, 'Incorrect tax calc', 'z:\TD\Escalations\ClientBackup\ASK011', 'P2', 'Not Started', '10/08/2022', NULL, 'Tax Desktop', 3);''')
print ("Tickets added successfully");

#commit changes
conn.commit()

#close the connection
conn.close()
