from chalice import Response

def update_mongo(description, location, place_id, col):
    result = col.insert({"description" : description, "location" : location, "place_id" : place_id})
    if result["nInserted"] != 1:
        return -1
    else:
        return 1

def description_search(keyword):
    col = get_mongo_conn()
    col.create_index([("description", "text")])

    docs = col.find({"$text": {"$search": keyword}}, {"score": {"$meta": "textScore"}})

    return docs

def location_search(location_name):
    col = get_mongo_conn()
    reg_location_name = "(" + location_name + ")" +"."

    docs = col.find({"location" : {"$regex" : reg_location_name}})

    return docs

def location_exact_match(location_query):
    col = get_mongo_conn()

    docs = col.find_one({"location" : location_query})

    return docs

def location_and_description(query):
    ids_to_show = []
    num_left = 25

    location_match = location_exact_match(query)
    if location_match != None:
        ids_to_show[0] = location_match["place_id"]
        num_left = num_left - 1
    
    location_reg = location_search(query)
    location_counter = 0
    for doc in location_reg:
        if location_counter == 5:
            break
        else:
            ids_to_show.append(doc["place_id"])
            location_counter = location_counter + 1
            num_left = num_left  - 1
    
    description_match = description_search(query)
    for descdoc in description_match:
        if num_left == 0:
            break
        else:
            ids_to_show.append(descdoc["place_id"])
            num_left = num_left  - 1
    
    return ids_to_show

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
