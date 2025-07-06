# Upload Photo Microservice

This project is a Python-based backend service for uploading and managing user photos. It uses Flask to provide a RESTful API endpoint for photo uploads, MongoDB as the database to store image data, and JWT for secure authentication.

## Folder Structure

The project is organized into the following main folders:

-   `.github/workflows/`: Contains GitHub Actions workflow files for Continuous Integration and Continuous Deployment (CI/CD). Specifically, it includes workflows for publishing Docker images.
-   `conections/`: Houses modules responsible for establishing and managing database connections. Currently, it includes `mongo.py` for connecting to a MongoDB instance.
-   `services/`: Contains the business logic of the application. For example, `functions.py` includes logic for processing and saving uploaded photos.
-   `tests/`: Includes all test files for the application. `route_test.py` provides an example of how to test the API endpoints.

## Backend Design Pattern

The backend follows a **Service Layer** (or N-Tier) architectural pattern. This is evident in the separation of concerns:
-   **API/Presentation Layer (`main.py`):** Handles HTTP requests, routing, and basic request validation.
-   **Service Layer (`services/functions.py`):** Encapsulates the core business logic, such as image validation, processing, and interaction with the data access layer.
-   **Data Access Layer (`conections/mongo.py`):** Manages communication with the database (MongoDB).

This separation makes the application more modular, maintainable, and testable.

## Communication Architecture

The application employs a **Client-Server** communication architecture:
-   **RESTful API:** The server exposes a RESTful API endpoint built using the Flask web framework. Clients interact with the server by sending HTTP requests to this API.
-   **Database Communication:** The `pymongo` library is used for communication between the application and the MongoDB database, where image metadata and a Base64 representation of the image are stored.
-   **Authentication:** Secure communication is ensured through **JSON Web Tokens (JWT)**. Clients must include a Bearer token in the `Authorization` header of their requests to access protected endpoints.

## API Endpoints

### `POST /upload-photo`

This endpoint allows authenticated users to upload a photo.

**Authentication:**

-   Requires a JWT Bearer token.
-   The token must be included in the `Authorization` header.
    ```
    Authorization: Bearer <your_jwt_token>
    ```

**Request:**

-   **Method:** `POST`
-   **Content-Type:** `multipart/form-data`
-   **Body:**
    -   `file`: The image file to be uploaded.
        -   Allowed file extensions: `png`, `jpg`, `jpeg`, `jfif`.
        -   The server also performs MIME type detection to ensure the file is a valid image.

**Responses:**

-   **`201 Created`**: Image uploaded successfully.
    ```json
    {
        "message": "Image uploaded successfully"
    }
    ```
-   **`400 Bad Request`**:
    -   If no file part is in the request:
        ```json
        {
            "error": "No file part in the request"
        }
        ```
    -   If no file is selected:
        ```json
        {
            "error": "No selected file"
        }
        ```
    -   If the file type is not allowed:
        ```json
        {
            "error": "File type not allowed"
        }
        ```
    -   If the file format is not supported (e.g., detected MIME type is not `image/png` or `image/jpeg`):
        ```json
        {
            "error": "File format not supported. Use PNG or JPG/JPEG"
        }
        ```
-   **`401 Unauthorized`**:
    -   If the token is missing or invalid:
        ```json
        {
            "error": "Token missing or invalid"
        }
        ```
    -   If the token data is invalid (e.g., missing `user_id`):
        ```json
        {
            "error": "Invalid token data"
        }
        ```
    -   If the token has expired:
        ```json
        {
            "error": "Token expired"
        }
        ```
    -   If the token is generally invalid:
        ```json
        {
            "error": "Invalid token"
        }
        ```
-   **`500 Internal Server Error`**: If an unexpected error occurs during the upload process.
    ```json
    {
        "error": "Failed to upload image: <error_details>"
    }
    ```
