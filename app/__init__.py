from flask import Flask
from flask_login import LoginManager
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
from app import routes, models

# @app.before_first_request
# def create_tables():
#     db.create_all()
# login_manager = LoginManager()
# login_manager.init_app(app)
# @app.route('/')
# def home():
#     # Instantiate a dummy authorizer for managing 'virtual' users
#     authorizer = DummyAuthorizer()

#     # Define a new user having full r/w permissions and a read-only
#     # anonymous user
#     authorizer.add_user('CS3103', '12345', '.', perm='elradfmwMT')
#     authorizer.add_anonymous(os.getcwd())

#     # Instantiate FTP handler class
#     handler = FTPHandler
#     handler.authorizer = authorizer

#     # Define a customized banner (string returned when client connects)
#     handler.banner = "pyftpdlib based ftpd ready."

#     # Specify a masquerade address and the range of ports to use for
#     # passive connections.  Decomment in case you're behind a NAT.
#     #handler.masquerade_address = '151.25.42.11'
#     #handler.passive_ports = range(60000, 65535)

#     # Instantiate FTP server class and listen on 0.0.0.0:2121
#     address = ('127.0.0.1', 2121)
#     server = FTPServer(address, handler)

#     # set a limit for connections
#     server.max_cons = 256
#     server.max_cons_per_ip = 5

#     # start ftp server
#     server.serve_forever()

if __name__ == '__main__':
    app.run(threaded=True, host='127.0.0.1')