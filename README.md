# OIDC Hosted Login + YooniK Face Authentication 

## Supported OIDCs Providers

[OneLogin](https://www.onelogin.com/) and [Okta](https://www.okta.com/).

## Flask Example
> Requires Python version 3.6.0 or higher.

This example shows how to use an OIDC Hosted login with YooniK Face Authentication in a Flask project.
The login is achieved through the authorization code flow.

Steps on this application:
1. User click in Login.
2. User is redirected to perform the OIDC-Hosted login.
3. User is redirected back to this application with an access code that is then exchanged for an access token. 
4. Token is validated.
5. User takes a selfie to perform a second-factor face authentication with YooniK.
6. User is logged in.

The user is enrolled in YooniK APIs in the first face authentication.
Once logged in the User is able to delete its YooniK account.
 
## Prerequisites

Before running this sample, you will need the following:

* An OIDC Provider account and custom application configured. We provide integration follow along documentation for easier tests, check `.\docs` folder.
* An YooniK account. If you do not already have one, you can sign up [here](https://www.yoonik.me/register). For a free trial e-mail us to [support@yoonik.me](mailto:support@yoonik.me).

## Running This Example

### Setting up the environment
To run this application, you first need to clone this repo:

```bash
git clone https://github.com/dev-yoonik/yoonik-okta-example-python.git
cd yoonik-okta-example-python
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

Copy the [`config.json.dist`](config.json.dist) to `config.json`:

```bash
cp config.json.dist config.json
```

### Configuration

[Okta](docs/okta.md) and [OneLogin](docs/onelogin.md) configuration instructions are available in this repository in the `.\docs` folder.

Once all is configured you can run the app.

### Run
Run the app server:

```
python run_app.py
```

Now navigate to `http://localhost:8080` in your browser.

If you see a home page that prompts you to log in, then things are working! 

### Known issues

> If you already have a Single Sign-On session with your OIDC provider, you may want to use your browser in incognito mode to test the flow from a blank slate. 

> In case you run into any issues to start the webcam for face authentication, you may have to run this server in **https** mode or change the host from **localhost** to **127.0.0.1** (both in configuration file and in your Provider Application configuration).

## Contact & Support

For more information, support and trial licenses please [contact us](mailto:support@yoonik.me) or join us at our [discord community](https://discord.gg/SqHVQUFNtN).