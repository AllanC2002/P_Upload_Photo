# services/functions.py
import base64
from flask import jsonify
from bson.objectid import ObjectId
from conections.mongo import conection_mongo
from werkzeug.utils import secure_filename
import imghdr

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

        # Detectar tipo real de la imagen para asegurar validez
        file_type = imghdr.what(None, h=file_content)
        if file_type not in ['png', 'jpeg']:
            return {"error": "File format not supported. Use PNG or JPG/JPEG"}, 400

        content_type = f"image/{file_type}"

        encoded_image = base64.b64encode(file_content).decode("utf-8")

        # Actualizar o insertar la imagen
        images_collection.update_one(
            {"Id_User": user_id},
            {"$set": {
                "name": filename,
                "image_base64": encoded_image,
                "description": "User uploaded image",
                "content_type": content_type
            }},
            upsert=True
        )
        return {"message": "Image uploaded successfully"}, 201

    except Exception as e:
        return {"error": f"Failed to upload image: {str(e)}"}, 500
