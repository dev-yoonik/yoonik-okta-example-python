import requests
import json

from bs4 import BeautifulSoup
from flask import Flask, render_template, redirect, request, url_for, jsonify
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from helpers import is_access_token_valid, is_id_token_valid, config
from user import User
from forms import FaceAuthenticationForm


app = Flask(__name__)
app.config.update({'SECRET_KEY': 'SomethingNotEntirelySecret'})

login_manager = LoginManager()
login_manager.init_app(app)


APP_STATE = 'ApplicationState'
NONCE = 'SampleNonce'


def allowed_base64_image(image_str):
    if not image_str.startswith('data:image/'):
        return False
    return image_str[11:14] in {'png', 'jpg', 'jpeg', 'gif'}


def parse_response_error(html_text: str) -> str:
    """Parse HTML error response
    :param html_text:
        HTML error message.
    :return:
        Parsed error message.
    """
    message = ''
    html = BeautifulSoup(markup=html_text, features="html.parser")
    if html.p:
        inner_html = BeautifulSoup(markup=html.p.text, features="html.parser")
        message = inner_html.text if inner_html.p is None else inner_html.p.text

    if "face_not_found" in message:
        message = "Could not find a face in the image."
    elif "multiple_faces" in message:
        message = "The image has more than one person."
    elif "quality_failed" in message:
        message = "The provided image does not have enough quality."
    else:
        message = "An error occurred. Please contact your systems administrator."
        print(f"ERROR: {html.text}")
    return message


def parse_response_status(status: str) -> str:
    """Create a message from the response status data
    :param status:
        Status of the operation.
    :return:
        Resulting message to be sent to the UI.
    """
    message = status
    if status == 'SUCCESS':
        message = "Face authentication successful"
    elif status == 'NEW_USER':
        message = "Face signup successful"
    elif status == 'USER_NOT_FOUND':
        message = "User not registered"
    elif status == 'FAILED':
        message = "Face authentication failed"
    return message


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
        base_url=config["auth_uri"],
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
        config["token_uri"],
        headers=headers,
        data=query_params,
        auth=(config["client_id"], config["client_secret"]),
    ).json()

    # Get tokens and validate
    if not exchange.get("token_type"):
        return "Unsupported token type. Should be 'Bearer'.", 403
    access_token = exchange["access_token"]
    id_token = exchange["id_token"]

    if not is_access_token_valid(access_token, config["issuer"]):
        return "Access token is invalid", 403

    if not is_id_token_valid(id_token, config["issuer"], config["client_id"], NONCE):
        return "ID token is invalid", 403

    # Authorization flow successful, get userinfo
    userinfo_response = requests.get(config["userinfo_uri"],
                                     headers={'Authorization': f'Bearer {access_token}'}).json()

    # Perform Face Authentication with YooniK API
    status = 'FAILED'
    message_class = 'text-danger'
    message = 'Face authentication failed'
    continue_url = url_for("login")

    if allowed_base64_image(form.user_selfie.data):
        yoonik_request_data = {
            'user_id': userinfo_response["sub"],
            'user_photo': form.user_selfie.data.split('base64,')[1],
            'create_if_new': True
        }
        response = requests.post(
            config["yoonik_authentication_api_url"],
            headers={'x-api-key': config["yoonik_authentication_api_key"]},
            json=yoonik_request_data
        )
        if response.ok:
            result = json.loads(response.text)
            status = result['status']
            message_class = 'text-success' if status == 'SUCCESS' or status == 'NEW_USER' else 'text-danger'
            message = parse_response_status(status)
        else:
            message = f'Ups! {parse_response_error(response.text)}'

    # Login user (if face authentication was successful)
    if status == 'SUCCESS' or status == 'NEW_USER':
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
        status=status,
        html=render_template("result.html", message_class=message_class, message=message,
                             continue_url=continue_url))


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(host="localhost", port=8080)
