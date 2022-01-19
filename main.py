from flask import Flask, render_template, redirect, request, url_for, jsonify, flash
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)

from utils.helpers import allowed_base64_image, parse_response_error, parse_response_status
from services import Yoonik
from services.providers import OktaProvider, OneLoginProvider
from services.user import User
from utils.forms import FaceAuthenticationForm
from config import Configuration


app = Flask(__name__)
app.config.update({'SECRET_KEY': 'SomethingNotEntirelySecret'})

login_manager = LoginManager()
login_manager.init_app(app)

global yoonik
global provider


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("home.html", provider=provider.name)


@app.route("/login")
def login():
    return redirect(provider.get_login_uri())


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

    code = request.args.get("code")
    if not code:
        return "The code was not returned or is not accessible", 403

    token = provider.get_token(code, request.base_url)
    if token is None:
        return "Unsupported token type. Should be 'Bearer'.", 403

    if not provider.is_token_valid(token):
        return "Token validation was unsuccessful .", 403

    user_info = provider.get_user_info(token)

    # Perform Face Authentication with YooniK API
    status = 'FAILED'
    message_class = 'text-danger'
    message = 'Face authentication failed'
    continue_url = url_for("login")

    if allowed_base64_image(form.user_selfie.data):
        authenticate, result = yoonik.authenticate(user_info["sub"], form.user_selfie.data.split('base64,')[1], True)
        if authenticate:
            status = result['status']
            message = parse_response_status(status)

            if status == 'SUCCESS' or status == 'NEW_USER':
                message_class = 'text-success'
                continue_url = url_for("profile")

                user = User.get(user_info["sub"])
                if not user:
                    User.create(user_info["sub"], user_info["given_name"], user_info["email"])
                    user = User.get(user_info["sub"])
                login_user(user)
        else:
            message = f'Ups! {parse_response_error(result)}'

    return jsonify(
        status=status,
        html=render_template("result.html", message_class=message_class, message=message,
                             continue_url=continue_url))


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/delete-yoonik-account")
@login_required
def delete_yoonik_account():
    deleted = yoonik.delete_account(current_user.id)
    if deleted:
        flash("User successfully deleted from YooniK APIs!", "success")
        return redirect(url_for("logout"))
    else:
        flash("Error deleting user.", "danger")

    return redirect(url_for("home"))


def instantiate_services():
    global yoonik, provider

    config = Configuration()
    yoonik = Yoonik(config.yk_authentication_uri, config.yk_authentication_key)

    provider_name = config.provider_name.lower()
    if provider_name == "okta":
        provider = OktaProvider(config)

    elif provider_name == "onelogin":
        provider = OneLoginProvider(config)

    else:
        raise Exception("Unsupported provider.")


if __name__ == '__main__':
    instantiate_services()
    app.run(host="localhost", port=8080)
