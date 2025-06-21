# services/functions.py
import base64
from flask import jsonify
from bson.objectid import ObjectId
from conections.mongo import conection_mongo
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def custom_photo(user_id, file):
    if file.filename == '':
        return {"error": "No selected file"}, 400

    if not allowed_file(file.filename):
        return {"error": "File type not allowed"}, 400

    try:
        db = conection_mongo()
        images_collection = db["Images"]

        filename = secure_filename(file.filename)
        file_content = file.read()
        encoded_image = base64.b64encode(file_content).decode("utf-8")

        new_image = {
            "Id_User": user_id,
            "name": filename,
            "image_base64": encoded_image,
            "description": "User uploaded image"
        }

        images_collection.insert_one(new_image)
        return {"message": "Image uploaded successfully"}, 201

    except Exception as e:
        return {"error": f"Failed to upload image: {str(e)}"}, 500
