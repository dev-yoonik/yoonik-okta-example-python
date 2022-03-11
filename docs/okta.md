# Okta + YooniK Face Authentication - configuration guide

## Overview

This document is intended to be use with [YooniK Sample App](https://github.com/dev-yoonik/yoonik-okta-example-python), in which the app login is performed 
using the Okta OIDC and YooniK second-factor facial authentication. Enhancing security and privacy while providing a friendly user experience.

## Prerequisites

This app integration has the following requirements:

*   An Okta Developer Account, you can sign up for one at [https://developer.okta.com/signup/](https://developer.okta.com/signup/).
    
*   An YooniK account, you can sign up [here](https://www.yoonik.me/register). E-mail us [support@yoonik.me](mailto:support@yoonik.me) for a free trial license.
    
*   A [Python](https://www.python.org) developer environment.
    

## Setting up Okta

### Create an App Integration

1. Sign in to your Okta developer account as a user with administrative privileges.
    
2. In the Admin Console, go to **Applications** > **Applications**.
    
3. Click **Create App Integration**.
   1. Choose **OpenID Connect** in the **Sign-in method** section.
   2. Choose **Web Application** as the **Application type** for your integration.
4. Click **Next**.
    
5. In **General Settings**, enter a **name** for your integration and (optionally) upload a logo.

6. In **Grant type** confirm that the **Authorization Code** is selected.

7. Set **Sign-in redirect URI** to `http://127.0.0.1:8080/authorization-code/callback`.

8. Set **Sign-out redirect URI** to `http://127.0.0.1:8080`.

9. In the **Assignments** tab for the app integration, assign the application to the desired users, groups or skip it.

10. Click **Save**.

> Have the **Client ID** and **Client Secret** in hand.


### OIDC Well-Known Configuration

To your base Okta domain append `/.well-known/openid-configuration` and go to the address. This contains the OIDC needed information for the next section.

In this JSON the following keys will be important, pay attention to its values. 

```json
{
  "issuer": "https://your-subdomain.okta.com",
  "authorization_endpoint": "https://your-subdomain.okta.com/oauth2/v1/authorize",
  "token_endpoint": "https://your-subdomain.okta.com/oauth2/v1/token",
  "userinfo_endpoint": "https://your-subdomain.okta.com/oauth2/v1/userinfo"
}
```

## Setting up the Flask App

Open the `config.json` file.

Set the **oidc_base_url** to the OIDC as a common base URL (similar to `https://your-subdomain.okta.com/oauth2/v1/`).

The **issuer_url** to the `issuer`.

Set **auth_url** to the part following the base URL in `authorization_endpoint`.

Set  **token_url** to the part following the base URL in `token_endpoint`.

Set **userinfo_url** to the part following the base URL in `userinfo_endpoint`.

Set **token_validation_url** to `null` (validation is performed using the Okta python SDK).

Set **client_id** and **client_secret** to its values.

Set **yoonik_authentication_api_url** and **yoonik_authentication_api_key**, if you don’t have, please contact us.

Your final result should look like this.

```json
{
  "oidc_base_url": "https://your-subdomain.okta.com/oauth2/v1/",
  "issuer_url": "https://your-subdomain.okta.com",
  "auth_url": "authorize",
  "token_url": "token",
  "token_validation_url": null,
  "userinfo_url": "userinfo",

  "redirect_url": "http://127.0.0.1:8080/authorization-code/callback",

  "client_id": "your-client-id",
  "client_secret": "your-client-secret",

  "yoonik_authentication_api_url": "yoonik-api-url",
  "yoonik_authentication_api_key": "your-yoonik-api-key"
}
```

> <span style="color:green">**You are now ready** to start testing your new app with Okta login and YooniK Face Authentication as a second-factor!</span>
## Additional Resources


*   [Okta Hosted Login + YooniK Face Authentication](https://github.com/dev-yoonik/yoonik-okta-example-python) example on Github.
    
*   Subscribe YooniK Face Authentication [here](https://www.yoonik.me/pricing).
    

## Contact & Support


For more information, support and trial licenses please [contact us](mailto:support@yoonik.me) or join us at our [discord community](https://discord.gg/SqHVQUFNtN).
