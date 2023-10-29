# AI Image Generator and Editor Python API

## Description

The AI Image Generator and Editor Python API is a versatile tool that leverages OpenAI's DALL-E2 image generation model. This API enables the creation and manipulation of images using AI-based algorithms. It allows image generation from text descriptions and offers AI-based editing for images. Additionally, it includes support for OAuth2 authentication and JWT tokens for client authentication and authorization.

## Features

### 1. Image Generation

The API provides the ability to generate images from text descriptions using the DALL-E2 model.

### 2. Image Editing

Users can edit images using AI algorithms provided by OpenAI, enabling creativity and customization.

### 3. Authentication

The API supports OAuth2 authentication and JWT tokens for client authorization and secure access.

## Directory Structure

The project directory structure is organized as follows:

- **Adiz_api_modules**: This folder contains the core modules of the API.
- **MainApp.py**: The main Python file serving as the entry point to the API.

### Modules

- **adiz_db.py**: Contains classes for interacting with the database.
- **adiz_image_generator.py**: Implements the image generation and editing functionalities using the OpenAI API.
- **adiz_key_manager.py**: Manages and validates API keys.
- **adiz_signin_manager.py**: Includes classes for JWT token generation, token management, and user login/logout procedures.
- **adiz_Oauth2Provider.py**: Manages OAuth2 authentication procedures, including acquiring user authentication URLs, exchanging codes for tokens, and obtaining user information.
- **adiz_api_log.py**: Handles logging functionalities, allowing the API to log informative and error messages.


## API Endpoints

The API provides several endpoints to perform specific actions:

- `/v1/signin`: Handles user login and authentication.
- `/v1/signout`: Manages user logout and token invalidation.
- `/v1/generate-image`: Generates AI-based images from text descriptions.
- `/v1/edit-image`: Edits images using AI algorithms.
- `/v1/referral-link`: Retrieves the referral link for users.
- `/v1/credit`: Fetches credit information for users.
- `/v1/doc`: Provides API documentation information.

## Requirements

To run the AI Image Generator and Editor Python API, ensure you have the following requirements met:

- **Python:** Python 3.6 or higher.
- **OpenAI Account:** Obtain an API key from OpenAI for access to the DALL-E2 image generation model.
- **Database:** Access to a MySQL database for user and token management.
- **OAuth Providers:** Credentials for OAuth providers (Google, Microsoft, Apple) to support sign-in/sign-up functionality.
- **Web Server:** Ability to host a Python application (e.g., Flask, WSGI) for serving the API endpoints.
- **Dependencies:** Make sure to install all necessary Python dependencies outlined in the `requirements.txt` file.


## Documentation

Explore comprehensive documentation for this API to get started:

## Installation Guide

To get started with the AI Image Generator and Editor Python API, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Addis777/Ai_image_generation_api.git
    ```

2. **Install the required dependencies:**

    ```bash
    cd Ai_image_generation_api
    pip install -r requirements.txt
    ```

3. **Configure your environment:**

    - Create a virtual environment if necessary.
    - Update the necessary configurations (API keys, database details, OAuth credentials) in the respective files: `adiz_key_manager.py`, `adiz_db.py`, `adiz_signin_manager.py`, and others as required.

4. **Run the API:**

    ```bash
    python MainApp.py
    ```

5. **Verify the setup:**

    The API will start running on `localhost` at port `90`. You can test the API endpoints using tools like Postman or by sending HTTP requests to `http://localhost:90`.

### API Reference

This AI Image Generator and Editor API provides the following endpoints:

#### `POST /v1/signin`

- **Description:** Accepts both code-based and signin-based requests. Generates authentication URLs for Google, Microsoft, or Apple sign-ins.
- **Request parameters:**
  - `sign_type`: Type of sign-in (code or signin).
  - `sign_to`: Sign-in provider (Google, Microsoft, or Apple).
  - Additional parameters based on the chosen provider.
- **Response:** Returns a URL for the corresponding sign-in provider.

#### `POST /v1/signout`

- **Description:** Logs out the user by revoking the access token.
- **Request parameters:**
  - `token`: Active user token for logout.
- **Response:** Success message or error message if logout fails.

#### `POST /v1/generate-image`

- **Description:** Generates AI images based on text descriptions.
- **Request parameters:**
  - `prompt`: Text description for image generation.
  - `size`: Image size for the generated images.
  - `numb`: Number of images to generate.
- **Response:** Returns generated AI images.

#### `POST /v1/edit-image`

- **Description:** Edits an image using an AI model.
- **Request parameters:**
  - `prompt`: Text description for image generation.
  - `image`: Original image for editing.
  - `mask_image`: Mask image for editing.
  - `size`: Image size for the edited images.
  - `numb`: Number of images to edit.
- **Response:** Returns the edited image.

#### `POST /v1/referral-link`

- **Description:** Fetches the referral code for the authenticated user.
- **Request parameters:**
  - `token`: Valid JWT token for the user.
- **Response:** User's referral code.

#### `POST /v1/credit`

- **Description:** Retrieves information about the user's available and earned credits.
- **Request parameters:**
  - `token`: Valid JWT token for the user.
- **Response:** Credit-related data.

#### `POST /v1/doc`

- **Description:** Fetches the API documentation.
- **Request parameters:**
  - `token`: Valid JWT token for the user.
- **Response:** API documentation.

Each endpoint requires specific parameters and provides responses in JSON format. Refer to the detailed API documentation for more information on utilizing these endpoints effectively.

## Data Types

The API utilizes the following data types for input and output:

- **Input Data Type**: HTTP POST.
- **Output Data Type**: JSON.


### Change Log

#### Version 1.0.0

- **Added**: Initial set of API endpoints for user authentication and image manipulation.
- **Updated**: Improved handling for error responses.
- **Fixed**: Bug in token expiration logic.
- **Changed**: Altered the user database structure.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License

MIT License

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS," WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE, AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES, OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT, OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

