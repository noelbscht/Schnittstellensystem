from flask import Flask, request, render_template, redirect, jsonify, session, url_for, make_response
from flask_cors import CORS, cross_origin
from flask_mysqldb import MySQL
from dotenv import load_dotenv
import os

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")
cors = CORS(app)

app.config['MYSQL_HOST'] = os.getenv("MYSQL_HOST")
app.config['MYSQL_USER'] = os.getenv("MYSQL_USER")
app.config['MYSQL_PASSWORD'] = os.getenv("MYSQL_PASSWORD")
app.config['MYSQL_DB'] = os.getenv("MYSQL_DB")

mysql = MySQL(app)
app.extensions['mysqldb'] = mysql

@app.route("/")
def index():
    from interface import interface
    from utils import file_content

    doc_path = os.path.join(app.root_path, "static", "documentation", "interface.drawio.html")
    return render_template("index.html",
                           routes=interface.get_routes(),
                           documentation=file_content(doc_path))


@app.route("/login")
def login():

    if not 'group' in request.args or request.args['group'] == 'user':
        session['group'] = "user"
        session['permissions'] = ""
    elif request.args['group'] == 'admin':
        session['group'] = "admin"
        session['permissions'] = "server.status"

    return redirect(url_for('index'))

@app.route("/impressum")
def impressum():
    return render_template("impressum.html")

@app.route("/datenschutz")
def datenschutz():
    return render_template("datenschutz.html")

@app.route("/cookies", methods=["PUT"])
def cookies():
    if not "X-COOKIES-Preference" in request.headers:
        """UNPROCESSABLE ENTITY  """
        return jsonify({
            "message": "missing header."
        }), 422

    # update cookies
    preferences = request.headers["X-COOKIES-Preference"]
    session['cookie_preferences'] = preferences
    return jsonify({
        "message": "ok"
    })

@cross_origin()
@app.route("/api", defaults={"path": None}, methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"])
@app.route("/api/<path:path>", methods=["POST", "GET", "PUT", "DELETE", "OPTIONS"])
def interface(path):
    from interface import interface as api

    if not path:
        return api.get_route("information").on_request()

    return api.handle_request(request, path)

@app.before_request
def before_request():
    if 'group' not in session:
        session['group'] = "user"

if __name__ == '__main__':
    app.run(port=8080, debug=True)
