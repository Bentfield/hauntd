from chalice import Response

def get_place(id, conn):
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Place WHERE place_id = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            return result
    finally:
        conn.close()


def delete_place(id, conn):
    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM PLACE WHERE place_id = %s"
            cursor.execute(query, (id,))
            conn.commit()
            return Response("")
    finally:
        conn.close()


def post_place(request, conn):
    json = request.json_body
    email = json["email"]
    place_name = json["place_name"]
    location_string = json["location_string"]
    description = json["description"]
    if "latitude" in json and "longitude" in json:
        lat_long = f"{json['latitude']} {json['longitude']}"
    else:
        lat_long = None
    try:
        with conn.cursor() as cursor:
            query = "INSERT INTO PLACE (email, place_name, address, lat_long, avg_rating, description) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (email, place_name, location_string, lat_long, 0, description))
            conn.commit()
            return Response("")
    finally:
        conn.close()

def patch_place(id, request, conn):
    json = request.json_body
    UPDATEABLE = set(["place_name", "address", "description", "lat_long"])
    if "latitude" in json and "longitude" in json:
        json["lat_long"] = f"{json['latitude']} {json['longitude']}"
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