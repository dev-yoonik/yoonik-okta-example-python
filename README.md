# Flask + Okta Hosted Login + YooniK Face Authentication Example

This example shows you how to use Flask to log in to your application with an Okta Hosted Login page.

The login is achieved through the [authorization code flow](https://developer.okta.com/authentication-guide/implementing-authentication/auth-code), where the user is redirected to the Okta-Hosted login page. After the user authenticates, he is redirected back to the application with an access code that is then exchanged for an access token. Then he will perform a second-factor face authentication with YooniK.

After a successful face authentication, the user is logged in to the application (the user is enrolled in YooniK APIs in the first face authentication).

The source code of this example is based on the [Flask Sample Applications for Okta](https://github.com/okta/samples-python-flask) repository. 
> Requires Python version 3.6.0 or higher.

## Prerequisites

Before running this sample, you will need the following:

* An Okta Developer Account, you can sign up for one at https://developer.okta.com/signup/.
* An Okta Application configured for Web mode. You can create one from the Okta Developer Console, and you can find instructions [here](https://developer.okta.com/authentication-guide/implementing-authentication/auth-code#1-setting-up-your-application).  When following the wizard, use the default properties.  They are designed to work with our sample applications.
* An YooniK account. If you do not already have one, you can signup [here](https://www.yoonik.me/register). To get a free trial please e-mail us to [support@yoonik.me](mailto:support@yoonik.me).

## Running This Example

To run this application, you first need to clone this repo:

```bash
git clone https://github.com/dev-yoonik/yoonik-okta-example-python.git
cd yoonik-okta-example-python
```

Then install dependencies:

```bash
pip install -r requirements.txt
```

Copy the [`client_secrets.json.dist`](client_secrets.json.dist) to `client_secrets.json`:

```bash
cp client_secrets.json.dist client_secrets.json
```

You now need to gather the following information from the Okta Developer Console:

- **Client ID** and **Client Secret** - These can be found on the "General" tab of the Web application that you created earlier in the Okta Developer Console.
- **Issuer** - This is the URL of the authorization server that will perform authentication.  All Developer Accounts have a "default" authorization server.  The issuer is a combination of your Org URL (found in the upper right of the console home page) and `/oauth2/default`. For example, `https://dev-1234.oktapreview.com/oauth2/default`.

Additionally, you need to gather the **YooniK API URL** and **YooniK API key** from your YooniK account dashboard.

Fill in the information that you gathered in the `client_secrets.json` file.

```json
{
  "auth_uri": "https://{yourOktaDomain}/oauth2/default/v1/authorize",
  "client_id": "{yourClientId}",
  "client_secret": "{yourClientSecret}",
  "redirect_uri": "http://localhost:8080/authorization-code/callback",
  "issuer": "https://{yourOktaDomain}/oauth2/default",
  "token_uri": "https://{yourOktaDomain}/oauth2/default/v1/token",
  "userinfo_uri": "https://{yourOktaDomain}/oauth2/default/v1/userinfo",
  "yoonik_authentication_api_url": "{{yoonikApiUrl}}",
  "yoonik_authentication_api_key": "{{yoonikApiKey}}"
}
```

Start the app server:

```
python main.py
```

Now navigate to http://localhost:8080 in your browser.

If you see a home page that prompts you to log in, then things are working! Clicking the **Log in** button will redirect you to the Okta hosted sign-in page.

You can log in with the same account that you created when signing up for your Developer Org. You can also use a known username and password from your Okta Directory.

**Note:** If you are currently using your Developer Console, you already have a Single Sign-On (SSO) session for your Org. You will be automatically logged into your application as the same user that is using the Developer Console. You may want to use an incognito tab to test the flow from a blank slate.

> In case you run into any issues to start the webcam for face authentication, you may have to run this server in **https** mode or change the host from **localhost** to **127.0.0.1** (both here and in your Okta Web Application configuration).

## Contact & Support

For more information, support and trial licenses please [contact us](mailto:support@yoonik.me) or join us at our [discord community](https://discord.gg/SqHVQUFNtN).