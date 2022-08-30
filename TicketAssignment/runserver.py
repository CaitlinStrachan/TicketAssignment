"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""
import os
from TicketSystem import app

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
    try:
        PORT = int(os.environ.get('PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(host=HOST, port=PORT)
