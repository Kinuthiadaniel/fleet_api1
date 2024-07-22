from dotenv import load_dotenv
load_dotenv()

import os
import random

from flask_migrate import Migrate
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from flask_restful import Api,Resource
from flask import request, session,make_response, jsonify
from flask_bcrypt import Bcrypt
from datetime import timedelta


from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required, current_user
# from app import Login
from models import db

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATABASE = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}")


app = Flask(__name__)
app.secret_key = b'Y\xf1Xz\x00\xad|eQ\x80t \xca\x1a\x10K'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config["JWT_SECRET_KEY"] = "fsbdgfnhgvjnvhmvh"+str(random.randint(1,1000000000000)) 
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_TOKEN_LOCATION"] = ["headers"]
app.config["SECRET_KEY"] = "JKSRVHJVFBSRDFV"+str(random.randint(1,1000000000000))
app.json.compact = False
CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

api = Api(app)