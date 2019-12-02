from chalice import Response


def get_place(id, conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Place WHERE place_id = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            return Response(result)
    finally:
        conn.close()


def delete_place(id, email, conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT email FROM Place WHERE place_id = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if result['email'] == email:
                query = "DELETE FROM Place WHERE place_id = %s"
                cursor.execute(query, (id,))
                conn.commit()
                return Response("")
            else:
                return Response("", status_code=403)
    finally:
        conn.close()


def post_place(request, username, email, conn):
    json = request.json_body
    place_name = json["place_name"]
    address = json["address"]
    description = json["description"]
    if "latitude" in json and "longitude" in json:
        latitude = f"{json['latitude']}"
        longitude = f"{json['longitude']}"
    else:
        latitude = None
        longitude = None
    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO User (user_name, email) VALUES (%s, %s)"
            cursor.execute(query, (username, email))
            conn.commit()
            query = "INSERT INTO Place (email, place_name, address, latitude, longitude, avg_rating, description) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (email, place_name, address, latitude, longitude, 0, description))
            conn.commit()
            return Response("")
    finally:
        conn.close()


def patch_place(id, request, email, conn):
    json = request.json_body
    UPDATEABLE = set(["place_name", "address", "description", "latitude", "longitude"])
    try:
        with conn.cursor() as cursor:
            query = "SELECT email FROM Place WHERE place_id = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            if result['email'] == email:
                for k, v in json.items():
                    if k in UPDATEABLE:
                        sqlpatch = f"UPDATE Place SET {k} = %s WHERE place_id = %s"
                        cursor.execute(sqlpatch, (v, id))
                conn.commit()
                return Response("")
            else:
                return Response("", status_code=403)
    finally:
        conn.close()
