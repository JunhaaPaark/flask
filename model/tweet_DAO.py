from sqlalchemy import text


class TweetDao:

    def __init__(self, database):
        self.db = database

    def insert_tweet(self, user_id, tweet):
        return self.db.execute(text("""
            INSERT INTO tweets (
                user_id,
                tweet
            ) VALUES (
                :user_id,
                :tweet
            )
            """), {
            'user_id': user_id,
            'tweet': tweet
        }).rowcount

    def get_timeline(self, user_id):
        result = self.db.execute(text("""
            SELECT
                t.tweet,
                t.user_id
            FROM tweets t
            LEFT JOIN follow_list fl

            ON fl.user_id = :user_id

            WHERE t.user_id = :user_id
            OR t.user_id = fl.follow_user_id
        """), {'user_id': user_id})

        timeline = result.fetchall()  # fetchall()로 data를 받아오면 python DS로 할당해주어야 함.

        '''
        timeline은 CursorResult 객체. 어디에선가 이 함수를 호출하여 리턴값을 파이썬 자료구조에 할당하여
        jsonify한 후 반환해주어야 한다.
        '''
        
        return [{
            'user_id': tweet['user_id'],
            'tweet': tweet['tweet']
        }
            for tweet in timeline]  # tweet은 t.tweet, t.user_id를 담고 있는 CursorResult

    
    
    
    
    