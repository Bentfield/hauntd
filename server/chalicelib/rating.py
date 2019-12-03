from chalice import Response

USER_CREATE = ("IF NOT EXISTS(SELECT email FROM User WHERE email = %s) "
            "BEGIN "
            "   INSERT INTO User (email, user_name) values (%s, %s) "
            "END")


def get_rating(id, conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Rating WHERE place_id = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            return result
    finally:
        conn.close()


def post_rating(request, email, username, conn):
    json = request.json_body
    place_id = json["place_id"]
    rating = json["rating"]
    try:
        rating = int(rating)
        if rating < 0 or rating > 5:
            return Response("Invalid rating range. Rating should be an integer value in the range [0, 5].", status_code=400)
        with conn.cursor() as cursor:
            cursor.execute(USER_CREATE, (email, email, username))
            conn.commit()
            query = ("INSERT INTO Rating (place_id, email, rating) "
                     "VALUES (%s, %s, %s) "
                     "ON DUPLICATE KEY UPDATE "
                     "rating = %s")
            res = cursor.execute(query, (place_id, email, rating, rating))
            conn.commit()
            return Response(res)
    finally:
        conn.close()