from chalice import Response
from pymongo import MongoClient
from collections import OrderedDict
import json

def get_spooked():
    col = get_mongo_conn()
    spooky_time = col.find_one({"$sample" : {"size" : 1}})

    return spooky_time


def insert_mongo(description, location, place_id, col):
    col.insert({"description" : description, "location" : location, "place_id" : place_id})


def update_mongo(description, location, place_id, col):
    col.update({"place_id": place_id}, {"place_id": place_id, "location" : location, "description" : description})


def delete_mongo(place_id, col):
    col.remove({"place_id" : place_id})


def get_description_from_id(place_id, col):
    doc = col.find_one({"place_id": place_id})
    return doc["description"]


def description_search(keyword, col):
    col.create_index([("description", "text")])
    docs = col.find({"$text": {"$search": keyword}}, {"score": {"$meta": "textScore"}})
    return docs


def location_search(location_name, col):
    reg_location_name = "(" + location_name + ")" +"."
    docs = col.find({"location" : {"$regex" : reg_location_name, "$options": "i"}})
    return docs


def location_exact_match(location_query, col):
    docs = col.find_one({"location" : location_query})
    return docs


def get_place(query_string, conn, col):
    query = query_string.get('query')
    if len(query) == 0:
        return get_filter(query_string, None, conn, col)

    places = OrderedDict()

    location_match = location_exact_match(query, col)
    if location_match != None:
        places[location_match["place_id"]] = location_match["description"]

    location_reg = location_search(query, col)
    for doc in location_reg:
        places[doc["place_id"]] = doc["description"]

    description_match = description_search(query, col)
    for descdoc in description_match:
        places[descdoc["place_id"]] = descdoc["description"]

    return get_filter(query_string, places, conn, col)


def get_place_id(id, conn, col):
    try:
        with conn.cursor() as cursor:
            query = "SELECT * FROM PlaceUser WHERE place_id = %s"
            cursor.execute(query, (id,))
            result = cursor.fetchone()
            result['description'] = get_description_from_id(result['place_id'], col)
            return Response(result)
    finally:
        conn.close()


def delete_place(id, email, conn, col):
    try:
        with conn.cursor() as cursor:
            query = "DELETE FROM Place WHERE place_id = %s AND email = %s"
            rows = cursor.execute(query, (id, email))
            conn.commit()
            if rows > 0:
                delete_mongo(int(id), col)
                return Response("")
            else:
                return Response("", status_code=403)
    finally:
        conn.close()


def post_place(request, username, email, conn, col):
    json = request.json_body
    place_name = json["place_name"]
    address = json["address"]
    description = json["description"]
    latitude = float(json["latitude"])
    longitude = float(json["longitude"])
    try:
        with conn.cursor() as cursor:
            # query = "INSERT INTO User (user_name, email) VALUES (%s, %s)"
            # cursor.execute(query, (username, email))
            # conn.commit()
            create_user = "INSERT IGNORE INTO User (user_name, email) VALUES (%s, %s)"
            cursor.execute(create_user, (username, email))
            conn.commit()
            query = "INSERT INTO Place (email, place_name, address, latitude, longitude, avg_rating) VALUES (%s, %s, %s, %s, %s, 0)"
            cursor.execute(query, (email, place_name, address, latitude, longitude))

            query = "SELECT * FROM Place WHERE place_name = %s ORDER BY place_id DESC"
            cursor.execute(query, (place_name))
            place_id = cursor.fetchone()["place_id"]
            conn.commit()
            insert_mongo(description, place_name, place_id, col)
            return Response("")
    finally:
        conn.close()


def patch_place(id, request, email, conn, col):
    json = request.json_body
    UPDATEABLE = set(["place_name", "address", "latitude", "longitude"])
    try:
        with conn.cursor() as cursor:
            for k, v in json.items():
                if k in UPDATEABLE:
                    sqlpatch = f"UPDATE Place SET {k} = %s WHERE place_id = %s AND email = %s"
                    rows = cursor.execute(sqlpatch, (v, id, email))
            conn.commit()
            update_mongo(json["description"], json["place_name"], int(id), col)
            return Response("")
    finally:
        conn.close()


def reorder_places(places, ids):
    if len(ids) == 0:
        return places
    reordered = []
    for id in ids:
        for place in places:
            if place['place_id'] == id:
                reordered.append(place)
    return reordered


def get_filter(query_string, unfiltered, conn, col):
    if unfiltered is not None and len(unfiltered) == 0:
        return Response("")
    radius = query_string.get('findNear')
    user_lat = json.loads(query_string.get('location'))['latitude']
    user_long = json.loads(query_string.get('location'))['longitude']
    email = query_string.get('createdBy')
    if int(user_lat) == -1 or int(radius) == 0:
        if unfiltered is not None:
            while len(unfiltered) > 25:
                unfiltered.popitem()
    ids = []
    if unfiltered is not None:
        for item in unfiltered.keys():
            ids.append(int(item))

    places = []
    with conn.cursor() as cursor:
        if unfiltered is None:
            if int(user_lat) == -1 or int(radius) == 0:
                sqlfilter = ("SELECT DISTINCT * "
                    "FROM PlaceUser "
                    "WHERE email = %s "
                    "LIMIT 25;")

                rows = cursor.execute(sqlfilter, (email))
            else:
                sqlfilter = ("SELECT DISTINCT *,"
                    "(3959 * "
                    "acos("
                    "sin(radians(%s)) * "
                    "sin(radians(latitude)) + "
                    "cos(radians(%s)) * "
                    "cos(radians(latitude)) * "
                    "cos(radians(longitude) - radians(%s)))) "
                    "AS distance "
                    "FROM PlaceUser "
                    "HAVING distance < %s "
                    "ORDER BY distance "
                    "LIMIT 25;")

                rows = cursor.execute(sqlfilter, (user_lat, user_lat, user_long, radius))
        else:
            if int(user_lat) == -1 or int(radius) == 0:
                sqlfilter = ("SELECT DISTINCT * "
                    "FROM PlaceUser "
                    "WHERE place_id IN %s "
                    "LIMIT 25;")

                rows = cursor.execute(sqlfilter, (ids,))
            else:
                sqlfilter = ("SELECT DISTINCT *,"
                    "(3959 * "
                    "acos("
                    "sin(radians(%s)) * "
                    "sin(radians(latitude)) + "
                    "cos(radians(%s)) * "
                    "cos(radians(latitude)) * "
                    "cos(radians(longitude) - radians(%s)))) "
                    "AS distance "
                    "FROM PlaceUser "
                    "WHERE place_id IN %s "
                    "HAVING distance < %s "
                    "ORDER BY distance "
                    "LIMIT 25;")

                rows = cursor.execute(sqlfilter, (user_lat, user_lat, user_long, ids, radius))

        for i in range(0, rows):
            place = cursor.fetchone()
            if email == '' or place['email'] == email:
                if unfiltered is not None:
                    place['description'] = unfiltered[place['place_id']]
                else:
                    place['description'] = get_description_from_id(place['place_id'], col)
                places.append(place)
                results = reorder_places(places, ids)
        conn.commit()
        if len(places) == 0:
            return Response("")
        return Response(results)
