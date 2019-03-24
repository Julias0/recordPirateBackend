from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from flask_cors import CORS

from Config.Security import authenticate, identity
from Resources.UserResource import UserRegister
from Resources.EventResource import EventResource
from Model.UserModel import UserModel

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'makraman'

api = Api(app)

jwt = JWT(app, authenticate, identity)

cors = CORS(app)

@app.before_first_request
def create_tables():
    db.create_all()

    # creation of the first admin
    user1 = UserModel('dhar', 'KalaChashma')
    user1.isAdmin = True

    user1.save_to_db()


api.add_resource(UserRegister, '/register')
api.add_resource(EventResource, '/event')

if __name__ == '__main__':
    from Config.db import db
    db.init_app(app)
    app.run(port=5000, debug=True)
