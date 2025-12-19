E-Commerce Backend API

Overview
This project is a RESTful backend API for an e-commerce application built using Flask.
It supports secure user authentication, product listing, and cart management.
The application follows clean REST principles and focuses on secure backend design.

--------------------------------------------------

Features
- User registration and login
- JWT-based authentication
- Protected routes for cart operations
- Product listing APIs
- SQLite database integration
- Secure password handling
- Deployed on Render cloud platform

--------------------------------------------------

Tech Stack
- Programming Language: Python
- Framework: Flask
- Authentication: JWT (JSON Web Tokens)
- Database: SQLite
- Deployment: Render (Gunicorn)
- Tools: Postman, Git, GitHub

--------------------------------------------------

How to Run Locally

Step 1: Clone the repository
git clone https://github.com/vigneshsai52/ecommerce-backend.git
cd ecommerce-backend

Step 2: Install dependencies
pip install -r requirements.txt

Step 3: Run the application
python app.py

The API will start running on:
http://127.0.0.1:5000

--------------------------------------------------

Authentication Flow
- Users register and login using API endpoints
- On successful login, a JWT token is generated
- Token must be included in request headers for protected routes

--------------------------------------------------

API Testing
- All APIs were tested using Postman
- JWT tokens were validated for protected endpoints

--------------------------------------------------

Deployment
- Deployed on Render using Gunicorn
- Environment configured for production-ready execution

--------------------------------------------------

Learning Outcomes
- Hands-on experience with REST API design
- Implemented secure authentication using JWT
- Understood backend deployment workflow
- Improved understanding of API testing and security basics
