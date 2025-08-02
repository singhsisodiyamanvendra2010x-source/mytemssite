from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# --- Load products from JSON file ---
PRODUCTS_FILE = 'products.json'

def load_products():
    if os.path.exists(PRODUCTS_FILE):
        with open(PRODUCTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_products(products):
    with open(PRODUCTS_FILE, 'w') as f:
        json.dump(products, f, indent=4)

# --- Routes ---
@app.route("/")
def home():
    products = load_products()
    return render_template("home.html", products=products)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/wishlist")
def wishlist():
    wishlist = []  # Empty initially
    return render_template("wishlist.html", wishlist=wishlist)

@app.route("/cart")
def cart():
    cart = []  # Empty initially
    total = 0
    return render_template("cart.html", cart=cart, total=total)

@app.route("/orders")
def orders():
    return render_template("orders.html")

# --- Admin Login ---
@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "mytems.in" and password == "mydrugsm1000":
            session["admin"] = True
            return redirect("/admin/dashboard")
        else:
            return "Invalid credentials"
    return render_template("login.html")

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect("/admin/login")
    products = load_products()
    return render_template("admin_dashboard.html", products=products)

@app.route("/admin/add", methods=["POST"])
def admin_add():
    if not session.get("admin"):
        return redirect("/admin/login")

    name = request.form["name"]
    price = request.form["price"]
    image_url = request.form["image_url"]

    new_item = {"name": name, "price": price, "image": image_url}

    products = load_products()
    products.append(new_item)
    save_products(products)

    return redirect("/admin/dashboard")

@app.route("/admin/delete/<int:index>")
def admin_delete(index):
    if not session.get("admin"):
        return redirect("/admin/login")

    products = load_products()
    if 0 <= index < len(products):
        products.pop(index)
        save_products(products)

    return redirect("/admin/dashboard")

# --- Logout ---
@app.route("/admin/logout")
def admin_logout():
    session.pop("admin", None)
    return redirect("/admin/login")

# --- Run App ---
if __name__ == "__main__":
    app.run(debug=True)
