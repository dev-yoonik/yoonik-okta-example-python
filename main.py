import requests

from flask import Flask, render_template, redirect, request, url_for, jsonify, flash
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from yk_utils.files import read_json_from_file
from yk_utils.apis import FaceAuthentication

from user import User
from forms import FaceAuthenticationForm


config = read_json_from_file(filename='./client_secrets.json')
face_authentication = FaceAuthentication(
    api_url=config["yoonik_authentication_api_url"],
    api_key=config["yoonik_authentication_api_key"]
)

app = Flask(__name__)
app.config.update({'SECRET_KEY': 'SomethingNotEntirelySecret'})

login_manager = LoginManager()
login_manager.init_app(app)


APP_STATE = 'ApplicationState'
NONCE = 'SampleNonce'


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login")
def login():
    # get request params
    query_params = {'client_id': config["client_id"],
                    'redirect_uri': config["redirect_uri"],
                    'scope': "openid email profile",
                    'state': APP_STATE,
                    'nonce': NONCE,
                    'response_type': 'code',
                    'response_mode': 'query'}

    # build request_uri
    request_uri = "{base_url}?{query_params}".format(
        base_url=config["authorization_endpoint"],
        query_params=requests.compat.urlencode(query_params)
    )

    return redirect(request_uri)


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/authorization-code/callback", methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        return render_template("take_selfie.html", form=FaceAuthenticationForm())

    form = FaceAuthenticationForm()
    if not form.validate_on_submit():
        return "Error in selfie submission", 400

    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    code = request.args.get("code")
    if not code:
        return "The code was not returned or is not accessible", 403
    query_params = {'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': request.base_url
                    }
    query_params = requests.compat.urlencode(query_params)
    exchange = requests.post(
        config["token_endpoint"],
        headers=headers,
        data=query_params,
        auth=(config["client_id"], config["client_secret"]),
    ).json()

    # Get access token
    if not exchange.get("token_type"):
        return "Unsupported token type. Should be 'Bearer'.", 403
    access_token = exchange["access_token"]

    # Authorization flow successful, get userinfo
    userinfo_response = requests.get(config["userinfo_endpoint"],
                                     headers={'Authorization': f'Bearer {access_token}'}).json()

    # Perform Face Authentication with YooniK
    result = face_authentication.request_face_authentication(
        user_id=userinfo_response["sub"],
        user_photo=form.user_selfie.data
    )

    # Login user (if face authentication was successful)
    continue_url = url_for("login")
    if result.status in ('SUCCESS', 'NEW_USER'):
        continue_url = url_for("profile")
        unique_id = userinfo_response["sub"]
        user_email = userinfo_response["email"]
        user_name = userinfo_response["given_name"]

        user = User(
            id_=unique_id, name=user_name, email=user_email
        )

        if not User.get(unique_id):
            User.create(unique_id, user_name, user_email)

        login_user(user)

    return jsonify(
        status=result.status,
        html=render_template("result.html", message_class=result.message_class,
                             message=result.message, continue_url=continue_url))


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/delete-yoonik-account")
@login_required
def delete_yoonik_account():
    success = face_authentication.request_account_deletion(user_id=current_user.id)
    if success:
        flash("YooniK account successfully deleted.", "success")
    else:
        flash("Error deleting user.", "danger")

    return redirect(url_for("logout"))


if __name__ == '__main__':
    app.run(host="localhost", port=8080)
