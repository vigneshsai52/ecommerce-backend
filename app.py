from flask import Flask, request, jsonify
import sqlite3
import jwt
import datetime
from functools import wraps

app = Flask(__name__)
@app.route("/")
def home():
    return "E-commerce Backend API is running"

app.config["SECRET_KEY"] = "supersecretkey"

# ---------------- DB ----------------
def get_db():
    conn = sqlite3.connect("ecommerce.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY,
        name TEXT,
        price INTEGER
    )
    """)

    cur.execute("""
    CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        product_id INTEGER
    )
    """)

    # insert products only once
    cur.execute("SELECT COUNT(*) FROM products")
    if cur.fetchone()[0] == 0:
        cur.executemany(
            "INSERT INTO products VALUES (?, ?, ?)",
            [
                (1, "Laptop", 50000),
                (2, "Phone", 20000),
                (3, "Headphones", 2000)
            ]
        )

    conn.commit()
    conn.close()

# ---------------- JWT PROTECTOR ----------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"error": "Token missing"}), 401

        try:
            data = jwt.decode(token, app.config["SECRET_KEY"], algorithms=["HS256"])
            current_user = data["username"]
        except:
            return jsonify({"error": "Token invalid"}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)",
            (data["username"], data["password"])
        )
        conn.commit()
    except:
        return jsonify({"error": "User already exists"}), 400
    finally:
        conn.close()

    return jsonify({"message": "User registered successfully"}), 201

# ---------------- LOGIN ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (data["username"], data["password"])
    )
    user = cur.fetchone()
    conn.close()

    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = jwt.encode(
        {
            "username": data["username"],
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        },
        app.config["SECRET_KEY"],
        algorithm="HS256"
    )

    return jsonify({"message": "Login successful", "token": token})

# ---------------- PRODUCTS ----------------
@app.route("/products", methods=["GET"])
def products():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    items = [dict(row) for row in cur.fetchall()]
    conn.close()
    return jsonify(items)

# ---------------- ADD TO CART ----------------
@app.route("/cart/add", methods=["POST"])
@token_required
def add_to_cart(current_user):
    data = request.get_json()
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO cart (username, product_id) VALUES (?, ?)",
        (current_user, data["product_id"])
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Product added to cart"})

# ---------------- VIEW CART (FIXED) ----------------
@app.route("/cart", methods=["GET"])
@token_required
def view_cart(current_user):
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT products.id, products.name, products.price
        FROM cart
        JOIN products ON cart.product_id = products.id
        WHERE cart.username=?
    """, (current_user,))

    items = cur.fetchall()
    conn.close()

    # 🔥 IMPORTANT FIX
    if not items:
        return jsonify({"message": "Cart is empty", "items": []})

    return jsonify([dict(i) for i in items])

# ---------------- RUN ----------------
if __name__ == "__main__":
    init_db()
    app.run()
