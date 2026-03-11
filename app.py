from flask import Flask, render_template, request, redirect, url_for, session


data = {
    "users": {
        "me9511": {
            "password": "000",
            "name": "Admin",    
            "address": "Veterans Village, Ipil Zamboanga Sibugay",
            "age": "14"
        },
        "Ralp": {
            "password": "ralph",
            "name": "Ralph Crimson E. Martinez",
            "address": "Makilas, Ipil, Zamboanga Sibugay",
            "age": "14"
        }

    },
    "sales": [
        {
            "id": 1,
            "description": "Bundle of Pancit Canton",
            "category": "C",
            "user": "Ralp",
            "price": "200"    
        }
    ]
}

app = Flask(__name__)
app.secret_key = "tnriscaimk"


saleCategories = ["A", "B", "C", "D"]
#Categories are still place holders for now.

@app.route("/users")
def users():
    if "username" not in session or session["username"] != "me9511":
        return redirect(url_for("homepage"))
    return render_template("users.html", users=data["users"])

@app.route("/")
def index():
    return redirect(url_for("login"))

@app.route("/register", methods=["GET", "POST"])
def register():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        confirm = request.form["confirm"]
        name = request.form["name"]
        address = request.form["address"]
        age = request.form["age"]

        if username == "":
            error = "Username cannot be empty."
        elif len(password) < 4:
            error = "Password must be at least 4 characters."
        elif password != confirm:
            error = "Passwords do not match."
        elif username in data["users"]:
            error = "Username already taken."
        elif name == "" or address == "" or age == "":
            error = "All fields are required."
        elif not age.isdigit():
            error = "Age must be a number."
        else:
            data["users"][username] = {
                "password": password,
                "name": name,
                "address": address,
                "age": age
            }
            return redirect(url_for("login"))

    return render_template("register.html", error=error, form=request.form)


@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username not in data["users"] or data["users"][username]["password"] != password:
            error = "Something went wrong."
        else:
            session["username"] = username
            return redirect(url_for("homepage"))

    return render_template("login.html", error=error, form=request.form)


@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("login"))

@app.route("/add_sale", methods=["POST"])
def addSale():
    if "username" not in session:
        return redirect(url_for("login"))

    description = request.form["description"]
    category = request.form["category"]
    username = session["username"]
    price = request.form["price"]

    sale = {
        "id": len(data["sales"]) + 1,
        "description": description,
        "category": category,
        "user": username,
        "price": price
    }
    data["sales"].append(sale)
    return redirect(url_for("homepage"))

@app.route("/homepage", methods=["GET"])
def homepage():
    if "username" not in session:
        return redirect(url_for("login"))
    
    username = session["username"]
    
    if username == "me9511":
        visibleSales = data["sales"]
    else:
        visibleSales = [sale for sale in data["sales"] if sale["user"] == username]
    
    return render_template("homepage.html", sales=visibleSales, categories=saleCategories)



if __name__ == "__main__":
    app.run(debug=True)