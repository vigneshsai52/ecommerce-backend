E-COMMERCE BACKEND API

A secure and scalable E-Commerce backend built using Flask, featuring JWT authentication,
RESTful APIs, and SQLite database. The application is deployed on Render cloud.

--------------------------------------------------

FEATURES
- User Registration and Login
- JWT-based Authentication
- Product Listing API
- Add to Cart and View Cart (Protected Routes)
- SQLite Database Integration
- Deployed on Render

--------------------------------------------------

TECH STACK
Backend: Python, Flask
Authentication: JSON Web Tokens (JWT)
Database: SQLite
Deployment: Render
Tools: Git, GitHub, Postman

--------------------------------------------------

API ENDPOINTS

POST    /register      -> Register new user
POST    /login         -> Login and get JWT token
GET     /products      -> Fetch product list
POST    /cart/add      -> Add product to cart (JWT required)
GET     /cart          -> View cart (JWT required)

--------------------------------------------------

AUTHENTICATION HEADER FORMAT

Authorization: Bearer <JWT_TOKEN>

--------------------------------------------------

LIVE DEPLOYED URL

https://ecommerce-backend-b9ra.onrender.com

--------------------------------------------------

RUN LOCALLY

pip install -r requirements.txt
python app.py

--------------------------------------------------


