from flask import Flask, render_template, request, jsonify, session
import time

app = Flask(__name__)
app.secret_key = "my_super_secret_key"

db = {
    "admin_pass": "Khani_1396",
    "users": [
        {"username": "user1", "password": "123", "remaining_traffic": "5.4 گیگابایت از ۱۰ گیگابایت"}
    ],
    "packages": [
        {"id": 1, "name": "یک‌روزه ۱ گیگابایت", "spec": "روزانه | ۱ گیگابایت", "price": 15000},
        {"id": 2, "name": "یک‌روزه ۲ گیگابایت", "spec": "روزانه | ۲ گیگابایت", "price": 20000},
        {"id": 3, "name": "یک‌روزه ۳ گیگابایت", "spec": "روزانه | ۳ گیگابایت", "price": 30000},
        {"id": 4, "name": "یک‌روزه ۵ گیگابایت (تخفیف ۱۰٪)", "spec": "روزانه | ۵ گیگابایت", "price": 45000},
        {"id": 5, "name": "یک‌روزه ۱۰ گیگابایت (تخفیف ۱۰٪)", "spec": "روزانه | ۱۰ گیگابایت", "price": 85000},
        {"id": 6, "name": "نامحدود یک‌روزه (۲ تا ۹ صبح)", "spec": "شبانه | ۲ تا ۹ صبح", "price": 50000},
        {"id": 7, "name": "هفتگی ۳ گیگابایت", "spec": "هفتگی | ۳ گیگابایت", "price": 30000},
        {"id": 8, "name": "هفتگی ۵ گیگابایت", "spec": "هفتگی | ۵ گیگابایت", "price": 50000},
        {"id": 9, "name": "هفتگی ۷ گیگابایت", "spec": "هفتگی | ۷ گیگابایت", "price": 70000},
        {"id": 10, "name": "هفتگی ۹ گیگابایت", "spec": "هفتگی | ۹ گیگابایت", "price": 90000},
        {"id": 11, "name": "هفتگی ۱۲ گیگابایت", "spec": "هفتگی | ۱۲ گیگابایت", "price": 140000},
        {"id": 12, "name": "ماهانه ۳ گیگابایت", "spec": "ماهانه | ۳ گیگابایت", "price": 30000},
        {"id": 13, "name": "ماهانه ۵ گیگابایت", "spec": "ماهانه | ۵ گیگابایت", "price": 65000},
        {"id": 14, "name": "ماهانه ۱۰ گیگابایت", "spec": "ماهانه | ۱۰ گیگابایت", "price": 130000},
        {"id": 15, "name": "ماهانه ۵۰ گیگابایت", "spec": "ماهانه | ۵۰ گیگابایت", "price": 600000},
        {"id": 16, "name": "ماهانه ۱۰۰ گیگابایت (۱۶٪ تخفیف)", "spec": "ماهانه | ۱۰۰ گیگابایت", "price": 1100000},
        {"id": 17, "name": "نامحدود ۲ تا ۹ صبح یک‌ماهه", "spec": "شبانه ماهانه | ۲ تا ۹ صبح", "price": 120000}
    ],
    "discounts": [{"code": "NOROOZ", "percent": 20}],
    "orders": [],
    "notifications": {} 
}

@app.route("/")
def buy_page():
    return render_template("buy.html")

@app.route("/admin")
def admin_page():
    return render_template("admin.html")

@app.route("/api/login", methods=["POST"])
def login():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    user = next((u for u in db["users"] if u["username"] == username and u["password"] == password), None)
    if user:
        session["user"] = username
        return jsonify({"status": "ok", "username": username})
    return jsonify({"status": "error", "message": "نام کاربری یا رمز عبور اشتباه است"}), 400

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json or {}
    username = data.get("username", "").strip()
    password = data.get("password", "").strip()
    if not username or not password:
        return jsonify({"status": "error", "message": "اطلاعات کامل نیست"}), 400
    if any(u["username"] == username for u in db["users"]):
        return jsonify({"status": "error", "message": "نام کاربری تکراری است"}), 400
    
    db["users"].append({"username": username, "password": password, "remaining_traffic": "نامشخص"})
    session["user"] = username
    return jsonify({"status": "ok", "username": username})

@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("user", None)
    return jsonify({"status": "ok"})

@app.route("/api/current-user", methods=["GET"])
def current_user():
    username = session.get("user")
    if not username:
        return jsonify({"user": None, "traffic": "", "has_notif": False})
    
    user_obj = next((u for u in db["users"] if u["username"] == username), {})
    traffic = user_obj.get("remaining_traffic", "ثبت نشده")
    
    notif_data = db["notifications"].get(username)
    has_notif = False
    if notif_data:
        if time.time() < notif_data["expire"]:
            has_notif = True
        else:
            del db["notifications"][username]
            
    return jsonify({"user": username, "traffic": traffic, "has_notif": has_notif, "notif_text": notif_data["text"] if has_notif else ""})

@app.route("/api/admin-login", methods=["POST"])
def admin_login():
    data = request.json or {}
    if data.get("password", "").strip() == db["admin_pass"]:
        session["admin"] = True
        return jsonify({"status": "ok"})
    return jsonify({"status": "error", "message": "رمز عبور مدیر اشتباه است"}), 401

@app.route("/api/check-admin", methods=["GET"])
def check_admin():
    return jsonify({"isAdmin": session.get("admin", False)})

@app.route("/api/packages", methods=["GET", "POST"])
def handle_packages():
    if request.method == "POST":
        data = request.json or {}
        db["packages"].append({
            "id": len(db["packages"]) + 1,
            "name": data.get("name"),
            "spec": data.get("spec"),
            "price": int(data.get("price", 0))
        })
        return jsonify({"status": "ok"})
    return jsonify(db["packages"])

@app.route("/api/packages/<int:pkg_id>", methods=["DELETE"])
def delete_pkg(pkg_id):
    db["packages"] = [p for p in db["packages"] if p["id"] != pkg_id]
    return jsonify({"status": "ok"})

@app.route("/api/discounts", methods=["GET", "POST"])
def handle_discounts():
    if request.method == "POST":
        data = request.json or {}
        db["discounts"].append({"code": str(data.get("code")).strip().upper(), "percent": int(data.get("percent", 0))})
        return jsonify({"status": "ok"})
    return jsonify(db["discounts"])

@app.route("/api/discounts/<string:code>", methods=["DELETE"])
def delete_discount(code):
    db["discounts"] = [d for d in db["discounts"] if d["code"] != code.upper()]
    return jsonify({"status": "ok"})

@app.route("/api/check-discount", methods=["POST"])
def check_discount():
    code = str((request.json or {}).get("code", "")).strip().upper()
    found = next((d for d in db["discounts"] if d["code"] == code), None)
    if found:
        return jsonify({"valid": True, "percent": found["percent"]})
    return jsonify({"valid": False, "message": "کد تخفیف معتبر نیست"})

@app.route("/api/orders", methods=["GET", "POST"])
def handle_orders():
    if request.method == "POST":
        if not session.get("user"):
            return jsonify({"status": "error", "message": "وارد شوید"}), 401
        data = request.json or {}
        db["orders"].append({
            "id": len(db["orders"]) + 1,
            "user": session["user"],
            "package": data.get("package"),
            "price": data.get("price"),
            "status": "در انتظار تایید"
        })
        return jsonify({"status": "ok"})
    return jsonify(db["orders"])

@app.route("/api/orders/<int:order_id>/status", methods=["POST"])
def update_order_status(order_id):
    status = request.json.get("status")
    target_order = None
    for o in db["orders"]:
        if o["id"] == order_id:
            o["status"] = status
            target_order = o
            break
            
    if target_order and status == "تایید شده":
        username = target_order["user"]
        db["notifications"][username] = {
            "text": f"🎉 سفارش بسته '{target_order['package']}' شما تایید و فعال شد!",
            "expire": time.time() + (12 * 3600)
        }
        
    return jsonify({"status": "ok"})

@app.route("/api/users", methods=["GET", "POST"])
def handle_users():
    if request.method == "POST":
        data = request.json or {}
        db["users"].append({
            "username": data.get("username"),
            "password": data.get("password"),
            "remaining_traffic": data.get("traffic", "نامشخص")
        })
        return jsonify({"status": "ok"})
    return jsonify(db["users"])

@app.route("/api/users/traffic", methods=["POST"])
def update_user_traffic():
    data = request.json or {}
    username = data.get("username")
    new_traffic = data.get("traffic")
    for u in db["users"]:
        if u["username"] == username:
            u["remaining_traffic"] = new_traffic
            break
    return jsonify({"status": "ok"})

@app.route("/api/users/<string:username>", methods=["DELETE"])
def delete_user(username):
    db["users"] = [u for u in db["users"] if u["username"] != username]
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
