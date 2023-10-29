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

To use this API, ensure you have:

- **Web Server**: Any web server supporting Python, such as Flask or WSGI.
- **Python Version**: 3.0 or higher.

## Documentation

Explore comprehensive documentation for this API to get started:

- [Installation Guide](#): Learn how to set up and install the API.
- [Tutorials](#): Understand the effective use of the API through various tutorials.
- [API Reference](#): Detailed information about the API endpoints and functions.
- [Data Types](#): Information about the data types used in the API.
- [Authentication Guide](#): Guidelines for client authentication and authorization using OAuth2 and JWT tokens.

## Changelog

Stay updated on the latest changes and improvements to the API:

- [Changelog](#): Check the full history of the AI Image Generator and Editor Python API.
