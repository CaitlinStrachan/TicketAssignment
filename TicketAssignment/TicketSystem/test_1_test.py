import os
from flaskr import flaskr
import pytest
import tempfile

class Test_test1_test(unittest.TestCase):
    def setUp(self):
        self.db_fd, flaskr.app.config['ticketdb.db'] = tempfile.mkstemp()
        flaskr.app.testing = True
        self.app = flaskr.app.test_client()
        with flaskr.app.app_context():
            flaskr.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(flaskr.app.config['ticketdb.db'])

    def login(self, email, password):
    return self.app.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)

    def test_login(self):
    rv = self.login('testadmin1@gmail.com', 'testpass')
    assert b'Logged in succesfully' in rv.data

if __name__ == '__main__':
    unittest.main()
