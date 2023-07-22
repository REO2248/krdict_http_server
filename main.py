from flask import Flask, request, redirect, render_template, send_from_directory
import flask_login
import sqlite3
import flask_wtf
import wtforms
import os
from dotenv import load_dotenv

try:
    load_dotenv()
    DICT_PATH=os.getenv('DICT_PATH')
    FONTS_PATH=os.getenv('FONTS_PATH')
    IMAGES_PATH=os.getenv('IMAGES_PATH')
    USERNAME=os.getenv('USER_NAME')
    PASSWORD=os.getenv('PASSWORD')
    SECRET_KEY=os.getenv('SECRET_KEY')
    HOST=os.getenv('HOST')
    PORT=os.getenv('PORT')
    DEBUG=os.getenv('DEBUG')
except:
    pass

app = Flask(__name__, template_folder=".", static_folder=".")
app.secret_key = SECRET_KEY
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

def noneexcept(string):
    if string is None:
        return ""
    return string
app.add_template_filter(noneexcept)

@app.route("/")
@flask_login.login_required
def main():
    return render_template("index.html")

class User(flask_login.UserMixin):
    def __init__(self, user_id):
        self.id = user_id

class LoginForm(flask_wtf.FlaskForm):
    user_id = wtforms.StringField(
            "user_id",
            [wtforms.validators.DataRequired()])
    password = wtforms.PasswordField(
            "password",
            [wtforms.validators.DataRequired()])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)

    if form.validate_on_submit():
        print(form.user_id.data, form.password.data)
        print(USERNAME, PASSWORD)
        if form.user_id.data == USERNAME and form.password.data == PASSWORD:
            print("songgong")
            user = User(form.user_id.data)
            flask_login.login_user(user)
            return redirect('/')
        else:
            return "가입실패"
    return render_template("login.html",form=form)

@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

@app.route("/logout", methods=["GET"])
def logout():
    flask_login.logout_user()
    return "가입탈퇴하였습니다. <a href=/>첫페지</a>"

@login_manager.unauthorized_handler
def unauthorized():
    return redirect('/login')

@app.route("/<id>")
@flask_login.login_required
def word_page(id=0):
    if id == 0:
        return "", 404
    conn = sqlite3.connect(DICT_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM AllWord WHERE id =?", (id,))
    result = c.fetchone()
    if result is None:
        return "", 404
    if result[3] is not None:#3:link_num
        return redirect("/"+str(result[3]))
    return render_template("word.html", title=result[1], body=result[6])

@app.route("/search", methods=["GET", "POST"])
@flask_login.login_required
def search():
    if request.method == "GET":
        return render_template("search.html")
    else:
        method= request.form["match-method"]
        skey = request.form["skey"]
        if method == "prefix":
            skey= skey+"%"
        elif method == "suffix":
            skey= "%"+skey
        elif method == "partial":
            skey = "%"+skey+"%"
        else:
            pass
        conn = sqlite3.connect(DICT_PATH)
        c = conn.cursor()
        sql = f"""
                SELECT *
                FROM AllWord
                WHERE special LIKE '{skey}'
                ORDER BY id
        """

        c.execute(sql)
        rows = c.fetchall()
        return render_template("search.html", rows=rows)

@app.route("/fonts/<font>")
@flask_login.login_required
def get_font(font):
    return send_from_directory(FONTS_PATH, font)

@app.route("/images/<image>")
@flask_login.login_required
def get_image(image):
    return send_from_directory(IMAGES_PATH, image)

@app.route("/favicon.ico")
def get_icon():
    return ""

@app.route("/style.css")
def get_style():
    return send_from_directory(".","style.css")

@app.errorhandler(404)
def page_not_found(e):
    return "404 Not Found"

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=DEBUG)