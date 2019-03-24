from flask_restful import Resource, reqparse
from Model.UserModel import UserModel
from Model.EventModel import EventModel
from flask_jwt import jwt_required


class EventResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('event',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    parser.add_argument('createdOn',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )

    def post(self):
        data = EventResource.parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        session = EventModel.find_session(user, data['createdOn'])

        if (session):
            session.event = data['event']
            session.save_to_db()

            return {"message": user.json(),
                    "payload": session.json()
                    }, 200
        else:
            session = EventModel(data['event'], data['createdOn'])
            session.user = user
            session.save_to_db()

        return {"message": user.json(),
                "payload": session.json()
                }, 200

    @jwt_required()
    def get(self):
        return {
            "payload": list(map(lambda x: x.json(),
                                list(EventModel.get_all_events())))
        }
