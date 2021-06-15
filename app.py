import dbconnect
import mariadb
import traceback
from flask import Flask, Response, request
import json
from flask_cors import CORS
# import bjoern

# set app to conect with Flask
app = Flask(__name__)
CORS(app)
# add the GET endpoint of candy
@app.get("/candy")

def get_candy():
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    candy = None
    try:
        # select all of the candy from the db and set to candy
        cursor.execute("SELECT name, id, description, image_url, price FROM candy")
        candy = cursor.fetchall()
    except:
        traceback.print_exc()
        print("something went wrong with the database")
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    # send back an error message or a proper response if everything above goes well
    if(candy == None):
        return Response("Failed to get candy from DB", mimetype="text/plain", status=500)
   
    else:
         # translate candy to json
        candy_json = json.dumps(candy, default=str)
        # return the json response for Post man
        return Response(candy_json, mimetype="application/json", status=200)
    
@app.post("/candy")

def post_candy():
    conn = None
    cursor = None
    new_id = -1
    try:
        candy_name = request.json['name']
        candy_desc = request.json['description']
        candy_price = request.json['price']
        candy_url = request.json['image_url']
    except:
        traceback.print_exc()
        print("There was a problem with the request")
        return Response("Data error", mimetype="text/plain", status=400)
    if(candy_name == None or candy_desc == None or candy_price == None or candy_url == None):
        return Response("Data error", mimetype="text/plain", status=400)
   
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    try:
        cursor.execute("INSERT INTO candy (name, description, price, image_url) VALUES (?, ?, ?, ?)", [candy_name, candy_desc, candy_price, candy_url])
        conn.commit()
        new_id = cursor.lastrowid
    except:
        traceback.print_exc()
        print("something went wrong with the database")
    # new_candy_json = json.dumps(new_candy, default=str)
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)
    if(new_id == -1):
        return Response("Failed to post candy", mimetype="text/plain", status=500)
    else:
        return Response(f"Successfully posted {candy_name}!", mimetype="text/plain", status=200)


@app.patch("/candy")

def patch_candy():
    conn = None
    cursor = None
    candy_id = None
    new_price = 0
    new_name = ""
    new_desc = ""
    new_image = ""
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)
    # your postman should look like something like this
    # {
    #     "idcandy": 14,
    #     "updatecandy": "Snow Owl"
    # }
    # request this JSON:
    try:
        candy_id = int(request.json['id'])
        new_price = int(request.json['newPrice'])
        new_name = str(request.json['newName'])
        new_desc = str(request.json['newDesc'])
        new_image = str(request.json['newImg'])


    except:
        traceback.print_exc()
        print("There was a problem with the request")

    try:
        # select the candy based on the id so we have the candy
        
        cursor.execute("SELECT name, id FROM candy WHERE id=?", [candy_id])
        # use fetchone because we selected by a single id
        old_candy = cursor.fetchone()[0]
    except:
        traceback.print_exc()
        print("There was a problem selecting the original candy name")
    try:
        # update the db with the updated candy and the candy id then commit
        if(new_price != 0):
            cursor.execute(f"UPDATE candy SET price=? WHERE id=?", [new_price, candy_id])
            conn.commit()
        if(new_name != ""):
            cursor.execute(f"UPDATE candy SET name=? WHERE id=?", [new_name, candy_id])
            conn.commit()
        if(new_desc != ""):
            cursor.execute(f"UPDATE candy SET description=? WHERE id=?", [new_desc, candy_id])
            conn.commit()
        if(new_image != ""):
            cursor.execute(f"UPDATE candy SET image_url=? WHERE id=?", [new_image, candy_id])
            conn.commit()
    except:
        traceback.print_exc()
        print("There was a problem updating candy name")

#    close connections
    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)

    # send back an error message or a proper response if everything above goes well
    # if(new_price == None or candy_id == None):
    #     return Response("Failed the patch request", mimetype="text/plain", status=400)
    # else:
    return Response(f"Succesfully updated {old_candy}", mimetype="text/plain", status=200)

@app.delete("/candy")
def delete_candy():
    conn = None
    cursor = None
    candy_id = -1
    conn = dbconnect.get_db_connection()
    cursor = dbconnect.get_db_cursor(conn)

    try:
        candy_id = int(request.json['candyId'])
    except:
        traceback.print_exc()
        print("There was a problem requesting the candy to be deleted")
    try: 
        # delete the candy from the database based on the id
        cursor.execute("DELETE FROM candy WHERE id=?", [candy_id])
        conn.commit()
    except:
        traceback.print_exc()
        print("There was a problem deletimg the name of the candy from the database")


    dbconnect.close_db_cursor(cursor)
    dbconnect.close_db_connection(conn)

    if(candy_id == -1):
        return Response("Faile to delete candy", mimetype="text/plain", status=500)
    else:
        return Response(f"Succesfully deleted", mimetype="text/plain", status=200)


app.run(debug=True)
# bjoern.run(app, "0.0.0.0", 5001)