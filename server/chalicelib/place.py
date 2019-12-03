from chalice import Response
from pymongo import MongoClient

def description_search(keyword):
    client = MongoClient("mongodb+srv://ssethia2:hauntd411@hauntdtext-ox5ai.mongodb.net/test?retryWrites=true&w=majority")

    db = client.Hauntd
    col = db.haunted_places

    col.create_index([("description", "text")])

    docs = col.find({"$text": {"$search": keyword}}, {"score": {"$meta": "textScore"}})

    return docs

def location_search(location_name):
    client = MongoClient("mongodb+srv://ssethia2:hauntd411@hauntdtext-ox5ai.mongodb.net/test?retryWrites=true&w=majority")

    db = client.Hauntd
    col = db.haunted_places

    reg_location_name = "(" + location_name + ")" +"."

    docs = col.find({"location" : {"$regex" : reg_location_name}})

    return docs

def location_exact_match(location_query):
    client = MongoClient("mongodb+srv://ssethia2:hauntd411@hauntdtext-ox5ai.mongodb.net/test?retryWrites=true&w=majority")

    db = client.Hauntd
    col = db.haunted_places

    reg_location_query = "(" + location_query + ")" +"."

    docs = col.find({"location" : reg_location_query})

    return docs

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
            query = "INSERT INTO Place (email, place_name, address, latitude, longitude, description) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (email, place_name, address, latitude, longitude, description))
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
