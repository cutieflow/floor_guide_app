from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os

app = Flask(__name__)
app.secret_key = "very_secret_key"  # セッション用の秘密鍵（実際は環境変数などで管理）

DATA_FILE = "data.json"

# シンプルな翻訳辞書（各文言のキーと日本語/英語の対応）
TRANSLATIONS = {
    "title": {"ja": "市役所庁舎 フロアガイド", "en": "City Hall Floor Guide"},
    "admin_title": {"ja": "管理画面", "en": "Admin Panel"},
    "login_title": {"ja": "管理者ログイン", "en": "Admin Login"},
    "login_username": {"ja": "ユーザー名", "en": "Username"},
    "login_password": {"ja": "パスワード", "en": "Password"},
    "login_button": {"ja": "ログイン", "en": "Login"},
    "logout_button": {"ja": "ログアウト", "en": "Logout"},
    "save_button": {"ja": "保存", "en": "Save"},
    "back_link": {"ja": "← 戻る", "en": "← Back"},
    "floor_list": {"ja": "フロア一覧", "en": "Floor List"},
    "floor_detail": {"ja": "フロア詳細", "en": "Floor Detail"},
    "services": {"ja": "サービス一覧", "en": "Services"},
    "image": {"ja": "画像", "en": "Image"},
    "map": {"ja": "地図", "en": "Map"},
    "add_or_edit_floor": {"ja": "フロア追加/編集", "en": "Add/Edit Floor"},
    "floor_id": {"ja": "フロアID（例：3F）", "en": "Floor ID (e.g., 3F)"},
    "floor_name": {"ja": "フロア名", "en": "Floor Name"},
    "services_hint": {
        "ja": "サービス一覧（1行1サービス）",
        "en": "Enter each service on a new line",
    },
    "image_url": {"ja": "画像URL", "en": "Image URL"},
    "map_url": {"ja": "地図URL", "en": "Map URL"},
    "description": {"ja": "詳細説明", "en": "Description"},
    "areas": {"ja": "エリア", "en": "Areas"},
    "area_id": {"ja": "エリアID", "en": "Area ID"},
    "area_name": {"ja": "エリア名", "en": "Area Name"},
    "area_description": {"ja": "エリア説明", "en": "Area Description"},
    "area_image": {"ja": "エリア画像URL", "en": "Area Image URL"},
    "add_area": {"ja": "エリアを追加", "en": "Add Area"},
}


def translate(text_id):
    lang = session.get("lang", "ja")
    return TRANSLATIONS.get(text_id, {}).get(lang, text_id)


def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# 言語切替用ルート
@app.route("/set_language/<lang>")
def set_language(lang):
    if lang in ["ja", "en"]:
        session["lang"] = lang
    return redirect(request.referrer or url_for("index"))


@app.route("/")
def index():
    floors = load_data()
    return render_template("index.html", floors=floors, translate=translate)


@app.route("/floor/<floor_id>")
def floor_detail(floor_id):
    floors = load_data()
    floor = floors.get(floor_id.upper())
    return render_template(
        "floor_detail.html", floor=floor, floor_id=floor_id.upper(), translate=translate
    )


# ログイン認証（簡易実装）
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        # シンプルな認証チェック
        if username == "admin" and password == "password":
            session["logged_in"] = True
            flash(
                "ログイン成功"
                if session.get("lang", "ja") == "ja"
                else "Login Successful"
            )
            return redirect(url_for("admin"))
        flash(
            "ユーザー名またはパスワードが間違っています"
            if session.get("lang", "ja") == "ja"
            else "Invalid credentials"
        )
    return render_template("login.html", translate=translate)


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("ログアウトしました" if session.get("lang", "ja") == "ja" else "Logged out")
    return redirect(url_for("index"))


# 管理画面：ログイン必須
@app.route("/admin", methods=["GET", "POST"])
def admin():
    if not session.get("logged_in"):
        return redirect(url_for("login"))
    floors = load_data()
    if request.method == "POST":
        floor_id = request.form["floor_id"].upper()
        description = request.form.get("description", "")
        name = request.form["name"]
        services = request.form["services"].splitlines()
        image = request.form.get("image", "").strip()
        map_url = request.form.get("map", "").strip()

        areas_json = request.form.get("areas_json", "{}")
        areas = json.loads(areas_json)

        floors[floor_id] = {
            "name": name,
            "description": description,
            "services": services,
            "image": image,
            "map": map_url,
            "area": areas,
        }
        save_data(floors)
        flash(
            "フロア情報を保存しました"
            if session.get("lang", "ja") == "ja"
            else "Floor data saved"
        )
        return redirect(url_for("admin"))
    return render_template("admin.html", floors=floors, translate=translate)


if __name__ == "__main__":
    app.run(debug=True)
