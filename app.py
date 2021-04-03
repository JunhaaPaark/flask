'''
app.py = 각 Layer를 이어 주는 역할!
https://dojang.io/mod/page/view.php?id=2450  패키지, 모듈 from import
'''


from flask import Flask
from sqlalchemy import create_engine
from flask_cors import CORS

from model import UserDao, TweetDao  # __init__.py의 __all__에서 지정
from service import UserService, TweetService
from view import create_endpoints


class Services:  # service 클래스들을 담고 있을 클래스
    pass

############################
# Create App
############################


def create_app(test_config=None):
    app = Flask(__name__)

    CORS(app)

    if test_config is None:
        app.config.from_pyfile("config.py")
    else:
        app.config.update(test_config)

    database = create_engine(app.config['DB_URL'], encoding='utf-8',
                             max_overflow=0)

    # Persistence Layer
    user_dao = UserDao(database)
    tweet_dao = TweetDao(database)

    # Business Layer
    services = Services  # 빈 클래스로 묶는 방법 -> create_endpoint에 단일 인자로 전달 가능
    services.user_service = UserService(user_dao, app.config)
    services.tweet_service = TweetService(tweet_dao)

    # Creates endpoints
    create_endpoints(app, services)

    return app


'''
Questions
1. create_app 함수를 호출하는 주체는?
2. return인 app은 어디로 가는가? WSGI? 미들웨어?
'''
