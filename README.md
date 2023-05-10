# Flask + Okta Hosted Login + Youverse Face Authentication Example

This example shows you how to use Flask to log in to your application with an Okta Hosted Login page.

The login is achieved through the [authorization code flow](https://developer.okta.com/authentication-guide/implementing-authentication/auth-code), where the user is redirected to the Okta-Hosted login page. After the user authenticates, he is redirected back to the application with an access code that is then exchanged for an access token. Then he will perform a second-factor face authentication with Youverse.

After a successful face authentication, the user is logged in to the application (the user is enrolled in Youverse APIs in the first face authentication).

The source code of this example is based on the [Flask Sample Applications for Okta](https://github.com/okta/samples-python-flask) repository. 
> Requires Python version 3.6.0 or higher.

## Prerequisites

Before running this sample, you will need the following:

* An Okta Account.
* Youverse app integration installed in your Okta instance (can be installed from the **App Catalog**).
* An Youverse account. If you do not already have one, you can signup [here](https://www.youverse.id/register). To get a free trial please e-mail us to [support@youverse.id](mailto:support@youverse.id).

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

You now need to gather the following information from the Okta Admin Console:

* **Client ID** and **Client Secret** - These can be found on the **Sign On** tab of the Youverse app integration that you installed earlier in the Okta Admin Console. 
* **Open ID Connect URLs** - These are the **authorization_endpoint**, **token_endpoint** and **userinfo_endpoint** for your Okta domain that can be found by clicking on **OpenID Provider Metadata** link under the **Sign On** tab.

Additionally, you need to gather the **Youverse API URL** and **Youverse API key** from your Youverse account dashboard.

Fill in the information that you gathered in the `client_secrets.json` file.

```json
{
  "authorization_endpoint": "https://{{yourOktaDomain}}/oauth2/v1/authorize",
  "client_id": "{{yourClientId}}",
  "client_secret": "{{yourClientSecret}}",
  "redirect_uri": "http://127.0.0.1:8080/authorization-code/callback",
  "token_endpoint": "https://{{yourOktaDomain}}/oauth2/v1/token",
  "userinfo_endpoint": "https://{{yourOktaDomain}}/oauth2/v1/userinfo",
  "yoonik_authentication_api_url": "{{providedApiUrl}}",
  "yoonik_authentication_api_key": "{{providedApiKey}}"
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

For more information, support and trial licenses please [contact us](mailto:support@youverse.id) or join us at our [discord community](https://discord.gg/SqHVQUFNtN).