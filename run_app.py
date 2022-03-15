""" OIDC Hosted Login + YooniK Face Authentication Flask Example """

from flask import Flask, render_template, redirect, request, url_for, jsonify, flash
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from yk_utils.apis import FaceAuthentication
from utils.config import Configuration
from services.providers import OktaProvider, OneLoginProvider
from utils.forms import FaceAuthenticationForm
from data_model.user import User

global YK_FACE_AUTHENTICATION, PROVIDER

app = Flask(__name__)
app.config.update({'SECRET_KEY': 'SomethingNotEntirelySecret'})

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


@app.route("/")
def home():
    return render_template("home.html", provider=config.provider_name)


@app.route("/login")
def login():
    return redirect(PROVIDER.get_login_url())


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)


@app.route("/authorization-code/callback", methods=['GET', 'POST'])
def callback():
    if request.method == 'GET':
        if "error" and "error_description" in request.args:
            return str(request.args["error_description"]), 409
        return render_template("take_selfie.html", form=FaceAuthenticationForm())

    form = FaceAuthenticationForm()
    if not form.validate_on_submit():
        return "Error in selfie submission", 400

    code = request.args.get("code")
    if not code:
        return "The code was not returned or is not accessible", 403

    token = PROVIDER.request_access_token(code, request.base_url)
    if token is None:
        return "Unsupported token type. Should be 'Bearer'.", 403

    if not PROVIDER.is_access_token_valid(token):
        return "Token validation was unsuccessful .", 403

    user_info = PROVIDER.get_user_info(token)

    # Perform Face Authentication with YooniK
    result = YK_FACE_AUTHENTICATION.request_face_authentication(
        user_id=user_info["sub"],
        user_photo=form.user_selfie.data
    )

    # Login user (if face authentication was successful)
    continue_url = url_for("login")
    if result.status in ('SUCCESS', 'NEW_USER'):
        continue_url = url_for("profile")
        unique_id = user_info["sub"]
        user_email = user_info["email"]
        user_name = user_info["given_name"]

        if not User.get(unique_id):
            User.create(unique_id, user_name, user_email)
        user = User.get(unique_id)

        login_user(user)

    return jsonify(
        status=result.status,
        html=render_template(
            "result.html",
            message_class=result.message_class,
            message=result.message,
            continue_url=continue_url)
    )


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/delete-yoonik-account")
@login_required
def delete_yoonik_account():
    success = YK_FACE_AUTHENTICATION.request_account_deletion(user_id=current_user.id)
    if success:
        flash("YooniK account successfully deleted.", "success")
    else:
        flash("Error deleting user.", "danger")

    return redirect(url_for("logout"))


if __name__ == '__main__':

    config = Configuration()
    YK_FACE_AUTHENTICATION = FaceAuthentication(config.yk_authentication_url,
                                                config.yk_authentication_key)

    provider_name = config.provider_name.lower()
    if provider_name == "okta":
        PROVIDER = OktaProvider(config)
    elif provider_name == "onelogin":
        PROVIDER = OneLoginProvider(config)

    app.run(host="localhost", port=8080)
