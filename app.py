from flask import Flask, render_template, request, redirect, session
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "super_secret_key_123"

app.config["UPLOAD_FOLDER"] = "static/uploads"


# ---------------- DATABASE ----------------

def get_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- HOME ----------------

@app.route("/")
def home():
    return render_template("index.html")


# ---------------- REGISTER ----------------

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO users(name,email,password,role) VALUES(?,?,?,?)",
            (name, email, password, "user")
        )

        conn.commit()

        session["user_name"] = name
        session["user_id"] = cur.lastrowid
        session["profile_pic"] = None
        session["role"] = "admin"

        conn.close()

        return redirect("/profile")

    return render_template("register.html")


# ---------------- POST LOST ITEM ----------------

@app.route("/post_lost", methods=["GET","POST"])
def post_lost():

    if "user_id" not in session:
        return redirect("/register")

    if request.method == "POST":

        item = request.form.get("item_name")
        desc = request.form.get("description")
        location = request.form.get("location")
        image = request.files.get("image")

        filename = None
        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO lost_items(user_id,item_name,description,location,image) VALUES(?,?,?,?,?)",
            (session["user_id"], item, desc, location, filename)
        )

        conn.commit()
        conn.close()

        return redirect("/search")

    return render_template("post_lost.html")


# ---------------- POST FOUND ITEM ----------------

@app.route("/post_found", methods=["GET","POST"])
def post_found():

    if "user_id" not in session:
        return redirect("/register")

    if request.method == "POST":

        item = request.form.get("item_name")
        desc = request.form.get("description")
        location = request.form.get("location")
        image = request.files.get("image")

        filename = None
        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        conn = get_db()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO found_items(user_id,item_name,description,location,image) VALUES(?,?,?,?,?)",
            (session["user_id"], item, desc, location, filename)
        )

        conn.commit()
        conn.close()

        return redirect("/search")

    return render_template("post_found.html")


# ---------------- SEARCH ----------------

@app.route("/search")
def search():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM lost_items")
    lost = cur.fetchall()

    cur.execute("SELECT * FROM found_items")
    found = cur.fetchall()

    conn.close()

    return render_template("search.html", lost=lost, found=found)


# ---------------- CLAIM ----------------

@app.route("/claim/<int:item_id>", methods=["GET","POST"])
def claim(item_id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT lost_items.*, users.name 
        FROM lost_items
        JOIN users ON lost_items.user_id = users.id
        WHERE lost_items.id = ?
    """, (item_id,))

    item = cur.fetchone()

    if request.method == "POST":

        message = request.form["message"]

        cur.execute(
            "INSERT INTO claims(item_id, claimer_id, message) VALUES(?,?,?)",
            (item_id, session["user_id"], message)
        )

        conn.commit()
        conn.close()

        return render_template("claim.html", item=item, success=True)

    conn.close()
    return render_template("claim.html", item=item)


# ---------------- PROFILE ----------------

@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/register")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id=?", (session["user_id"],))
    user = cur.fetchone()

    cur.execute("SELECT voucher_name, voucher_value FROM vouchers WHERE user_id=?", (session["user_id"],))
    vouchers = cur.fetchall()

    conn.close()

    return render_template("profile.html", user=user, vouchers=vouchers)




# ---------------- EDIT PROFILE ----------------

@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():

    if "user_id" not in session:
        return redirect("/register")

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":

        course = request.form.get("course")
        year = request.form.get("year")
        reg_no = request.form.get("reg_no")

        image = request.files.get("profile_pic")

        if image and image.filename != "":
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

            cur.execute("""
                UPDATE users 
                SET course=?, year=?, reg_no=?, profile_pic=?
                WHERE id=?
            """, (course, year, reg_no, filename, session["user_id"]))

            session["profile_pic"] = filename
        else:
            cur.execute("""
                UPDATE users 
                SET course=?, year=?, reg_no=?
                WHERE id=?
            """, (course, year, reg_no, session["user_id"]))

        conn.commit()
        conn.close()

        return redirect("/profile")

    # GET request
    cur.execute("SELECT course, year, reg_no, profile_pic FROM users WHERE id=?",
                (session["user_id"],))
    user = cur.fetchone()

    conn.close()

    return render_template("edit_profile.html", user=user)




# ---------------- UPLOAD PROFILE PIC ----------------

@app.route('/upload_profile_pic', methods=['POST'])
def upload_profile_pic():

    if "user_id" not in session:
        return redirect("/register")

    file = request.files.get("profile_pic")

    if not file or file.filename == "":
        return redirect("/profile")

    filename = str(session["user_id"]) + "_" + secure_filename(file.filename)

    file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        UPDATE users
        SET profile_pic=?
        WHERE id=?
    """, (filename, session["user_id"]))

    conn.commit()
    conn.close()

    session["profile_pic"] = filename

    return redirect("/profile")



# ---------------- USERS ----------------
@app.route("/users")
def users():

    if "user_id" not in session:
        return redirect("/register")

    if session.get("role") != "admin":
        return "Access Denied ❌"

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT id, name, email FROM users")
    users = cur.fetchall()

    conn.close()

    return render_template("users.html", users=users)






# ---------------- REWARD ----------------

@app.route("/reward")
def reward():

    if "user_id" not in session:
        return redirect("/register")

    conn = get_db()
    cur = conn.cursor()

    # total vouchers
    cur.execute(
        "SELECT COUNT(*) FROM vouchers WHERE user_id=?",
        (session["user_id"],)
    )
    total_vouchers = cur.fetchone()[0]

    # items returned (approved claims)
    cur.execute(
        "SELECT COUNT(*) FROM claims WHERE claimer_id=? AND status='approved'",
        (session["user_id"],)
    )
    items_returned = cur.fetchone()[0]

    # leaderboard
    cur.execute("""
        SELECT u.name, COUNT(v.id) as total
        FROM users u
        LEFT JOIN vouchers v ON u.id = v.user_id
        GROUP BY u.id
        ORDER BY total DESC
        LIMIT 5
    """)
    leaderboard = cur.fetchall()

    conn.close()

    return render_template(
        "reward.html",
        total_vouchers=total_vouchers,
        items_returned=items_returned,
        leaderboard=leaderboard
    )




# ---------------- MY ITEMS ----------------

@app.route("/my_items")
def my_items():

    if "user_id" not in session:
        return redirect("/register")

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM lost_items WHERE user_id=?", (session["user_id"],))
    items = cur.fetchall()

    conn.close()

    return render_template("my_items.html", items=items)


# ---------------- ADMIN ----------------

@app.route("/admin")
def admin():

    if "user_id" not in session:
        return redirect("/register")

    if session.get("role") != "admin":
        return "Access Denied ❌"

    conn = get_db()
    cur = conn.cursor()

    cur.execute("SELECT * FROM claims WHERE status='pending'")
    claims = cur.fetchall()

    conn.close()

    return render_template("admin_dashboard.html", claims=claims)


# ---------------- SETTINGS ----------------

@app.route("/settings", methods=["GET","POST"])
def settings():

    if "user_id" not in session:
        return redirect("/register")

    if session.get("role") != "admin":
        return "Access Denied ❌"

    conn = get_db()
    cur = conn.cursor()

    if request.method == "POST":
        name = request.form.get("voucher_name")
        value = request.form.get("voucher_value")

        cur.execute(
            "UPDATE settings SET voucher_name=?, voucher_value=? WHERE id=1",
            (name, value)
        )
        conn.commit()

    cur.execute("SELECT voucher_name, voucher_value FROM settings WHERE id=1")
    data = cur.fetchone()

    conn.close()

    return render_template("settings.html", data=data)


# ---------------- APPROVE ----------------

@app.route("/approve/<int:claim_id>")
def approve(claim_id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("UPDATE claims SET status='approved' WHERE id=?", (claim_id,))

    cur.execute("SELECT claimer_id FROM claims WHERE id=?", (claim_id,))
    user = cur.fetchone()

    if user:
        cur.execute("SELECT voucher_name, voucher_value FROM settings WHERE id=1")
        setting = cur.fetchone()

        cur.execute(
            "INSERT INTO vouchers(user_id, voucher_name, voucher_value) VALUES(?,?,?)",
            (user["claimer_id"], setting["voucher_name"], setting["voucher_value"])
        )

    conn.commit()
    conn.close()

    return redirect("/admin")


# ---------------- REJECT ----------------

@app.route("/reject/<int:claim_id>")
def reject(claim_id):

    conn = get_db()
    cur = conn.cursor()

    cur.execute("UPDATE claims SET status='rejected' WHERE id=?", (claim_id,))

    conn.commit()
    conn.close()

    return redirect("/admin")


# ---------------- LOGOUT ----------------

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)