import base64
from flask import jsonify
from bson.objectid import ObjectId
from conections.mongo import conection_mongo
from werkzeug.utils import secure_filename
import filetype

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg','jfif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def custom_photo(user_id, file):
    try:
        print(">>> File...")
        print(">>> Name:", file.filename)
        print(">>> Content-Type:", file.content_type)

        if file.filename == '':
            return {"error": "No selected file"}, 400

        if not allowed_file(file.filename):
            return {"error": "File type not allowed"}, 400

        db = conection_mongo()
        images_collection = db["Images"]

        filename = secure_filename(file.filename)

        file_content = file.read()
        print(">>> Bytes leídos:", len(file_content))

        # Detect the file type with filetype
        kind = filetype.guess(file_content)
        print(">>> Tipo detectado:", kind.mime if kind else "No detectado")

        if not kind or kind.mime not in ['image/png', 'image/jpeg']:
            return {"error": "File format not supported. Use PNG or JPG/JPEG"}, 400

        content_type = kind.mime

        encoded_image = base64.b64encode(file_content).decode("utf-8")

        # Update or insert the image in the database
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

        print(">>> Imagen subida correctamente.")
        return {"message": "Image uploaded successfully"}, 201

    except Exception as e:
        print(">>> Error durante subida:", str(e))
        return {"error": f"Failed to upload image: {str(e)}"}, 500
