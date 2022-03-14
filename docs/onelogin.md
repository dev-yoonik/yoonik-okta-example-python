# OneLogin + YooniK Face Authentication - configuration guide

## Overview

This document is intended to be use with [YooniK Sample App](https://github.com/dev-yoonik/yoonik-okta-example-python), in which the app login is performed 
using the OneLogin OIDC and YooniK second-factor facial authentication. Enhancing security and privacy while providing a friendly user experience.

## Prerequisites

This app integration has the following requirements:

*   An OneLogin Developer Account, you can sign up here [https://www.onelogin.com/developer-signup](https://www.onelogin.com/developer-signup).
    
*   An YooniK account, you can sign up [here](https://www.yoonik.me/register). E-mail us [support@yoonik.me](mailto:support@yoonik.me) for a free trial license.
    
*   A [Python](https://www.python.org) developer environment.
    

## Setting up OneLogin

### Create an OpenID Connect app integration

1. Log in to your OneLogin account with administrative privileges.
    
2. Go to Adminstration page, click **Applications** > **Custom Connector**. 
    
3. In Custom Connector click **New Connector**.

4. Choose a **name** (example: YooniK 2 FA) for the connector. It’s optional to upload icons.
5. In **Sign on Method** select **OpenID Connect**.
6. In OpenID Connect section:
   1. Set **Redirect URI** to `http://127.0.0.1:8080/authorization-code/callback`. 
   This is where  OneLogin redirects the user after login along with the one time code generated.
   2. Set **Post Logout Redirect URI** to `http://127.0.0.1:8080`. 
   This is where OneLogin redirects the user when the application requests OneLogin logout.
   3. Set **Signing Algorithm** to `RS256`. This is the algorithm used to sign the JSON Web Token (JWT).
7. Set **Login URL** to `http://127.0.0.1:8080`. This is where the user is sent to when initializing the application from the OneLogin.
8. Click **Save**

### Create and configure a new application

Now it’s time to create a new application and associate it with the configured connector.

1. Next to Save click **More options** > **Add app to connector**.
2. You can specify the **display name** of your application. Uploading icons and filling description is optional.
3. Click **Save**.

Now that the application is created we need to get vital information for this example.

1. Open your new application configuration, and go to Single Sign-On (SSO) section. Here you have access to:
   1. **Client ID** and **Client Secret** - our sample app access credentials to use the OIDC API.
   2. **Well-know configuration** - details about the OIDC service.
2. Set **Application Type** to **Web**.
3. In the **Token Endpoint**, set **Authentication Method** as **Basic**.
4. **Users** tab registers the users with access to this application. Make sure you have at least one user account, to be used in when running the application.
5. Click **Save**

> Have the **Client ID** and **Client Secret** in hand.


### OIDC Well-Known Configuration

Open the **Well-known Configuration** hyperlink, you will need the following information.

In this JSON the following keys will be important, pay attention to its values. 

```json
{
  "authorization_endpoint": "https://your-subdomain.onelogin.com/oidc/2/auth",
  "token_endpoint": "https://your-subdomain.onelogin.com/oidc/2/token",
  "userinfo_endpoint": "https://your-subdomain.onelogin.com/oidc/2/me",
  "introspection_endpoint": "https://your-subdomain.onelogin.com/oidc/2/token/introspection"
}
```

## Setting up the Flask App

Open the `config.json` file.

1. Set the **oidc_base_url** to the OIDC as a common base URL (similar to `https://your-subdomain.onelogin.com/oidc/2/`).

2. Set **auth_url** to the part following the base URL in `authorization_endpoint`.

3. Set  **token_url** to the part following the base URL in `token_endpoint`.

5. Set **userinfo_url** to the part following the base URL in `userinfo_endpoint`.

6. Set **token_validation_url** to the part following the base URL in `introspection_endpoint`.

7. Set **client_id** and **client_secret** to its values.

8. Set **yoonik_authentication_api_url** and **yoonik_authentication_api_key**, if you don’t have, please contact us.

Your final result should look like this.

```json
{
  "oidc_base_url": "https://your-subdomain.onelogin.com/oidc/2/",
  "auth_url": "auth",
  "token_url": "token",
  "userinfo_url": "me",
  "token_validation_url": "token/introspection",

  "redirect_url": "http://127.0.0.1:8080/authorization-code/callback",

  "client_id": "your-client-id",
  "client_secret": "your-client-secret",

  "yoonik_authentication_api_url": "yoonik-api-url",
  "yoonik_authentication_api_key": "your-yoonik-api-key"
}
```

> <span style="color:green">**You are now ready** to start testing your new app with OneLogin login and YooniK Face Authentication as a second-factor!</span>
## Additional Resources

* Subscribe YooniK Face Authentication [here](https://www.yoonik.me/pricing).
* Sign up for a free developer account [OneLogin Developers: Start Building Today!](https://developers.onelogin.com/)
* Authorization Code Flow [OpenID Connect Auth Code Flow pt. 1 - OneLogin API](https://developers.onelogin.com/openid-connect/api/authorization-code)
* JWT Access Token Validation [JWT Access Token Validation](https://developers.onelogin.com/authentication/tools/jwt)

## Contact & Support

For more information, support and trial licenses please [contact us](mailto:support@yoonik.me) or join us at our [discord community](https://discord.gg/SqHVQUFNtN).
