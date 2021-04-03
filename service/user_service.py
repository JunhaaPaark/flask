'''
business layer의 UserService 클래스는 persistance layer의 UserDao에 의존한다.

DAO: Data Access Object (데이터 접속을 담당하는 객체)
DAO 객체들을 통해 DB 처리를 한다.

service 클래스들은 DAO 클래스들에 의존한다.
'''

import bcrypt
from datetime import datetime, timedelta
import jwt
from flask import jsonify


class UserService:

    def __init__(self, user_dao, config):
        self.user_dao = user_dao
        self.config = config

    def create_new_user(self, new_user):
        new_user['password'] = bcrypt.hashpw(
            new_user['password'].encode('UTF-8'),
            bcrypt.gensalt()
        )

        new_user_id = self.user_dao.insert_user(new_user)

        return new_user_id  # user_DAO를 사용하여 불러온 user_id를 (그대로) 리턴
        # new_user_id는 AUTO_INCREMENT되는 mysql 테이블의 id이다(lastrowid)

    def check_password(self, credential):
        email = credential['email']
        password = credential['password']

        account_info = self.user_dao.get_user_id_and_password(email)

        if account_info and bcrypt.checkpw(password.encode('UTF-8'),
                                           account_info['hashed_password'].encode('UTF-8')):
            return account_info
        return None

    def generate_token(self, user_id):

        payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(seconds=60*60*24)
        }
        token = jwt.encode(payload, self.config['JWT_SECRET_KEY'],
                           algorithm=self.config['ALGORITHM'])
        # return token.decode('UTF-8')  # decode를 하지 말아야 한다?? -> 해야 한다. (to string?)
        return token.decode('utf-8')

    def user_id_does_exist(self, user_id):
        if self.user_dao.check_user_id(user_id) is None:
            return False
        else:
            return True

    def follow(self, user_id, follow_id):
        return self.user_dao.insert_follow(user_id, follow_id)

    def unfollow(self, user_id, follow_id):
        return self.user_dao.insert_unfollow(user_id, follow_id)
