from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token

_user_parser= reqparse.RequestParser()
_user_parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
_user_parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be blank."
                        )
    

class UserRegister(Resource):
    
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(data['username'], data['password'])
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class UserLogin(Resource):
    
    @classmethod
    def post(cls):

        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])

        if user and safe_str_cmp(user.password,data['password']):
            access_token = create_access_token(identity = user.id,fresh=True)
            
            return {
                'access_token':access_token,
                
            },200

        return {"message":"Invalid credentials"},401
