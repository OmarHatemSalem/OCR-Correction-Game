
from flask import Flask, jsonify, request, make_response
import json, sqlite3

from kraken_images import transcribe
import os

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

# define the predict endpoint
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    fileObject = open("data.json", "r")
    jsonContent = fileObject.read()
    aList = json.loads(jsonContent) if jsonContent else []

    aList.append(data)
    jsonString = json.dumps(aList)
    jsonFile = open("data.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()

    transcribe.processBook(data["directory"])

    return jsonify(aList)

# define a route with GET method
@app.route('/books', methods=['GET'])
def getBooks():
    fileObject = open("data.json", "r")
    jsonContent = fileObject.read()
    aList = json.loads(jsonContent)

    return jsonify(aList)

@app.route('/books/<int:item_id>', methods=['GET'])
def getBook(item_id):
    # Perform logic to retrieve item with the specified ID
    # You can use the 'item_id' parameter to query your data source
    
    fileObject = open("data.json", "r")
    jsonContent = fileObject.read()
    aList = json.loads(jsonContent)

    aBook = aList[item_id]

    # Example response
    item = {
        'id': item_id,
        'name': aBook["name"],
        'images' : aBook["directory"]+"\\txt_kraken"
    }

    filename = os.listdir(aBook["directory"]+"\\txt_kraken")[0]
    f = os.path.join(aBook["directory"], filename)
    if os.path.isfile(f):
            item["next_image"] = f
    
    return item


# Temporary data store

@app.route('/books/<int:id>', methods=['PUT'])
def your_route(id):
    # Access the request data
    data = request.get_json()

    transcribe.update_dataset(data, id)
    # Return a response (optional)
    return jsonify({'message': f'PUT request received for ID {id}'})


if __name__ == '__main__':
    app.run()

