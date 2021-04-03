from flask import jsonify, request, Response, current_app, g
from flask.json import JSONEncoder
import bcrypt
import jwt
from functools import wraps
from flask_cors import CORS

# Defines each endpoint

'''
로직: request input data 처리 -> 로직 -> response output data 처리
'''
'''
뭐 코드가 훨씬 더 간단해진다거나 그러지는 않았다.
단지 service layer 관련 코드를 함수 인자로 외부에서 받아온다는 논리 계층이 형성된 것.


'''


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        # 나중에 JSONEncoder 클래스 원본 소스 코드의 수정사항을 이곳에 반영하기.

        return JSONEncoder.default(self, obj)


def login_required(f):  # check access_toke
    @wraps(f)
    def decorated_function(*args, **kwargs):
        access_token = request.headers.get('Authorization')
    # f는 어떻게 쓰였는가?
    # *args, **kwargs는 언패킹되지 않았다.

    # Decorator에 f 함수를 넣어 f의 기능을 확장하는 용도로 사용한 것이 아닌,
    # Decorator 구조의 껍데기만 이용해 추가 기능 구현하는 용도로 사용
    # 엔드포인트 함수 호출 전 특정 함수(로그인)를 먼저 호출하는 로직
    # 보다 구체적으로, g 객체의 user_id 속성에 access token의 user_id를 대입
        if access_token is not None:
            try:
                payload = jwt.decode(access_token,
                                     current_app.config['JWT_SECRET_KEY'],
                                     current_app.config['ALGORITHM'])
            except jwt.InvalidTokenError:  # /timeline 엔드포인트에서 InvalidTokenError가 뜬다. 왜?
                # InvalidTokenError이라 함은 decode에 실패했다는 것.
                # access_token은 Authorization 헤더에서 가져온 것이고.
                # 이 헤더는 tweets.js에서 쿠키로부터 가져온 것이고,
                # 이 쿠키는 login.js에서 만든 것이다.
                # access_token 자체는 login 엔드포인트 - user_service.generate_token에서 만들어짐.
                payload = None

            if payload is None:
                return Response(status=401)  # 여기 오류.

            g.user_id = payload['user_id']

        else:
            return Response(status=401)

        return f(*args, **kwargs)  # f를 리턴하는 의미를 생각해보기.
    return decorated_function


def create_endpoints(app, services):
    CORS(app)  # 이 구문이 app.py에만 있어서 문제가 됐던 것일까?
    # --> 추가해도 여전히 CORS 에러가 뜬다.
    # --> Client side의 문제인가?

    user_service = services.user_service
    tweet_service = services.tweet_service

    @app.route("/ping", methods=['GET'])
    def ping():
        return "pong"

    @app.route("/sign-up", methods=['POST'])
    def sign_up():
        new_user = request.json  # payload: user_id, password
        new_user_id = user_service.create_new_user(new_user)

        return jsonify(new_user_id)

    @app.route("/login", methods=['POST'])
    def login():
        credential = request.json
        account_info = user_service.check_password(credential)  # id, hashed_pw JSON or None
        '''
        <example>
        account_info = {
        'id': 2,
        'hashed_password': $2b$12$Z/WT7eEVfoCDX/wF.EQESeCv.OPOsIl/hXVwLVZaoo4WPnhDSOwCa
        }
        '''
        if account_info is not None:
            access_token = user_service.generate_token(account_info['id'])
        else:
            return Response(status=401)
        return jsonify({  # login.js의 msg가 이 JSON 데이터이다.
            'user_id': account_info['id'],
            'access_token': access_token  # decoding된 access_token / decode를 하지 말아야 하나?
        })  # 이 리턴값은 쓰이는 곳이 없다. (토큰정보는 리퀘스트의 Autorization 헤더에서 직접 가져오기 때문)

    @app.route("/follow", methods=['POST'])
    @login_required
    def follow():
        payload = request.json
        # user_id = payload['user_id']
        user_id = g.user_id  # login_required 데코레이터 정의할 때 할당된다.
        follow_id = payload['follow']

        if user_service.user_id_does_exist(follow_id) is False:
            return 'NoSuchUser', 400
        else:
            user_service.follow(user_id, follow_id)
            return Response(status=200)

    @app.route("/unfollow", methods=['POST'])
    @login_required
    def unfollow():
        payload = request.json
        user_id = g.user_id
        follow_id = payload['follow_id']

        if user_service.user_id_does_exist(follow_id) is False:
            return 'NoSuchUser', 400
        else:
            user_service.unfollow(user_id, follow_id)
            return Response(status=200)

    @app.route("/tweet", methods=['POST'])
    @login_required
    def tweet():
        payload = request.json
        user_id = payload['id']
        tweet = payload['tweet']
        if tweet_service.tweet(user_id, tweet) is None:
            return 'Too Long', 400
        # tweet_service.tweet(user_id, tweet)

        return Response(status=200)

    @app.route("/timeline", methods=['GET'])  # 여기서 401 error
    @login_required
    def get_timeline():
        timeline = tweet_service.timeline(g.user_id)
        return jsonify({
            'user_id': g.user_id,
            'timeline': timeline
        })

'''
    @app.route("/timeline/<int:user_id>", methods=['GET'])
    def timeline(user_id):
        timeline = tweet_service.timeline(user_id)
        return jsonify({
            'user_id': user_id,
            'timeline': timeline
        })
'''
