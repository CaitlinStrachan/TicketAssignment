import unittest
from TicketSystem import app, views
from flask import Flask, render_template
import json
import sqlite3 as sql
import os
import hashlib


class Test_test_1(unittest.TestCase):   

    def test_home_route(self):
        app = Flask(__name__, template_folder='TicketSystem/templates')
        with app.app_context():
            client = views.home()
            #client = app.home()
            url = '/'
            
            response = client.get(url)        
            assert response.status_code == 200

    def test_login(self):
         app = Flask(__name__, template_folder="templates")        
         with app.app_context():
            conn = sql.connect('ticketdb.db')
            conn.row_factory = sql.Row
            #views.login()
            data = {"email":"testadmin1@gmail.com","password":"testpass"}
            response = views.login().post("/login/", data)
            assert response.status_code == 200 
            assert response.json()["email"] == "testadmin1@gmail.com"
            assert response.json()["logged_in"] == True
        
if __name__ == '__main__':
    unittest.main()
