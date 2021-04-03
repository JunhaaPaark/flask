class TweetService:
    def __init__(self, tweet_dao):
        self.tweet_dao = tweet_dao

    def tweet(self, user_id, tweet):
        if len(tweet) > 300:
            return None

        return self.tweet_dao.insert_tweet(user_id, tweet)
    # insert_tweet() 메서드의 호출을 리턴한다. (__init__에서 호출된다)
    # tweet_DAO의 insert_tweet에서, execute()을 통해 실행되고 .rowcount를 반환한다.
    # __init__의 엔드포인트에서 rowcount가 할당(되지만 변수에 대입되지는 않아 사실상 소멸된다)
    # => 이 로직 다시 한 번 확인해보기.

    def timeline(self, user_id):
        return self.tweet_dao.get_timeline(user_id)
