from chalice import Response

def get_place(id, conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM PlaceRating WHERE place_id = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            return result
    finally:
        conn.close()


def delete_place(id, conn):
    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM Place WHERE place_id = %s"
            cursor.execute(query, (id,))
            conn.commit()
            return Response("")
    finally:
        conn.close()


def post_place(request, conn):
    json = request.json_body
    email = json["email"]
    place_name = json["place_name"]
    address = json["address"]
    description = json["description"]
    latitude = json["latitude"] if "latitude" in json else None
    longitude = json["longitude"] if "longitude" in json else None
    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO Place (email, place_name, address, latitude, longitude, avg_rating, description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (email, place_name, address, latitude, longitude, 0, description))
            conn.commit()
            return Response("")
    finally:
        conn.close()


def patch_place(id, request, conn):
    json = request.json_body
    UPDATEABLE = set(["place_name", "address", "description", "latitude", "longitude"])
    try:
        with conn.cursor() as cursor:
            for k, v in json.items():
                if k in UPDATEABLE:
                    sqlpatch = f"UPDATE Place SET {k} = %s WHERE place_id = %s"
                    cursor.execute(sqlpatch, (v, id))
            conn.commit()
            return Response("")
    finally:
        conn.close()