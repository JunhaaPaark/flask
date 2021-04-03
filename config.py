'''
config.py - DATABASE configuration file

mysqlconnector DBAPI 사용
'''
db = {
    'user': 'root',
    'password': 'halfrhgm99',
    # 'host': '0.0.0.0',  # for localhost mysql server
    'host': 'flask-twitter.ccw5f2kcbwdq.ap-northeast-2.rds.amazonaws.com',
    'port': 3306,
    # 'database': 'flask_API'  # for localhost mysql server
    'database': 'flask'
}

DB_URL = f"mysql+mysqlconnector://{db['user']}:{db['password']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"
# DB_URL = f"mysql+mysqlconnector://root:halfrhgm99@0.0.0.0:3306/flask_API?charset=utf8"

JWT_SECRET_KEY = "secretkey123"

ALGORITHM = 'HS256'
# mysql --host=13.125.244.160 --port=51148

# Junha - test1234
# Jennie - hellojenny
# JJJ - JJJ@gmail.com - JJJ