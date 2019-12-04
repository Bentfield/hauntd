from chalice import Response
import json


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
            query = "DELETE FROM Place WHERE place_id = %s AND email = %s"
            rows = cursor.execute(query, (id, email))
            conn.commit()
            if rows > 0:
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
            create_user = "INSERT IGNORE INTO User (user_name, email) VALUES (%s, %s)"
            cursor.execute(create_user, (username, email))
            conn.commit()
            query = "INSERT INTO Place (email, place_name, address, latitude, longitude, avg_rating) VALUES (%s, %s, %s, %s, %s, 0)"
            cursor.execute(query, (email, place_name, address, latitude, longitude))
            conn.commit()
            return Response("")
    finally:
        conn.close()


def patch_place(id, request, email, conn):
    json = request.json_body
    UPDATEABLE = set(["place_name", "address", "description", "latitude", "longitude"])
    try:
        with conn.cursor() as cursor:
            for k, v in json.items():
                if k in UPDATEABLE:
                    sqlpatch = f"UPDATE Place SET {k} = %s WHERE place_id = %s AND email = %s"
                    rows = cursor.execute(sqlpatch, (v, id, email))
            conn.commit()
            if rows > 0:
                return Response("")
            else:
                return Response("", status_code=403)
    finally:
        conn.close()


def get_filter(query_string, unfiltered, conn):
    radius = query_string.get('findNear')
    user_lat = json.loads(query_string.get('location'))['latitude']
    user_long = json.loads(query_string.get('location'))['longitude']
    email = query_string.get('createdBy')
    places = []
    if len(unfiltered) == 0:
        try:
            with conn.cursor() as cursor:
                sqlfilter = ("SELECT *,"
                    "(3959 * "
                    "acos("
                    "sin(radians(%s)) * "
                    "sin(radians(latitude)) + "
                    "cos(radians(%s)) * "
                    "cos(radians(latitude)) * "
                    "cos(radians(longitude) - radians(%s)))) "
                    "AS distance "
                    "FROM Place "
                    "HAVING distance < %s "
                    "ORDER BY distance")

                rows = cursor.execute(sqlfilter, (user_lat, user_lat, user_long, radius))
                for i in range(0, rows):
                    place = cursor.fetchone()
                    if email == '' or place['email'] == email:
                        places.append(place)
                conn.commit()
                return Response(places)
        finally:
            conn.close()
    # else:
