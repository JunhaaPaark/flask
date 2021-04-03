from sqlalchemy import text

'''
SQL functions defined as methods of a DAO Class.
'''


class UserDao:

    def __init__(self, database):
        self.db = database

    def insert_user(self, user):  # user는 user info에 관한 request를 의미함.
        return self.db.execute(text("""
            INSERT INTO profiles (
                name,
                email,
                hashed_password
            ) VALUES (
                :name,
                :email,
                :password
            )
            """), user).lastrowid

    def get_user_id_and_password(self, email):
        row = self.db.execute(text("""
            SELECT
                id,
                hashed_password
            FROM profiles
            WHERE
                email = :email
        """), {'email': email}).fetchone()

        return {
            'id': row['id'],
            'hashed_password': row['hashed_password']
        } if row else None  # 그냥 return row 하는 것과의 차이점이 있나?

    def insert_follow(self, user_id, follow_id):
        return self.db.execute(text("""
            INSERT INTO follow_list (
                user_id,
                follow_user_id
            ) VALUES (
                :user_id,
                :follow_user_id
            )
        """), {
            'user_id': user_id,
            'follow_user_id': follow_id
        }).rowcount

    def insert_unfollow(self, user_id, follow_id):
        return self.db.execute(text("""
            DELETE FROM follow_list
            WHERE user_id = :user_id
            AND follow_user_id = :follow_id
        """), {
            'user_id': user_id,
            'follow_user_id': follow_id
        }).rowcount

    def check_user_id(self, user_id):
        row = self.db.execute(text("""
            SELECT
                id
            FROM profiles
            WHERE id=:id"""), {'id': user_id}).fetchone()

        return {'id': row['id']} if row else None



