Image Metadata Analysis


1. Introduction

This Flask-based web application allows users to upload images and extract metadata, storing the information in a structured database. The app provides user authentication, image upload functionality, metadata extraction, and database storage, ensuring an organized and retrievable log of image metadata.


2. Features and Functionality


a. User Authentication

Implements user login and registration using Flask-Login.

Secure password storage with hashing.


b. Image Upload & Metadata Extraction

Users can upload images via a web interface.

Extracts metadata such as file format, size, dimensions, device details, and timestamps.

Stores metadata in JSON format for easy retrieval.


c. Database Storage

SQLAlchemy is used as the ORM.

Two primary models: User (authentication) and Image (metadata storage).

Establishes relationships to associate images with users.


d. User Dashboard

Displays uploaded images and corresponding metadata.

Provides options to download metadata.



3. Technology Stack

Backend: Flask, Flask-Login, SQLAlchemy

Frontend: HTML, Bootstrap

Database: SQLite (can be switched to PostgreSQL or MySQL)

Metadata Extraction: Python libraries (e.g., Pillow, ExifRead)




4. API & Security Measures

Implements session management for user authentication.

Protects routes with login requirements.

Secure database queries to prevent SQL injection.




5. Deployment Considerations

Can be deployed on cloud platforms like AWS, Heroku, or DigitalOcean.

Uses a requirements file for dependency management.



6. Future Enhancements

Filtering & Sorting: Improve metadata querying with filters.

Editing Metadata: Allow users to update metadata fields.

Enhanced UI: Improve responsiveness with Tailwind CSS.






HOW TO RUN?


Create a Virtual Environment

python3 -m venv venv


source venv/bin/activate



Install Dependencies


pip install -r requirements.txt


Run the App

python run.py
