# Okta + YooniK Face Authentication - configuration guide

## Overview

This integration guide configures a custom Web Application using the Okta Sign-in Widget and YooniK Face Authentication APIs to demonstrate how to add a second-factor authentication to Okta login flow, enhancing security and privacy while providing a seamless user experience.

## Contents

* Supported features
* Requirements
* Configuration steps
* Notes

## Supported features

* Service Provider (SP)-Initiated Authentication (SSO) Flow - This authentication flow occurs when the user attempts to log in from YooniK application.

## Prerequisites

This app integration has the following requirements:

* An Okta Account.
* An YooniK account. If you do not already have one, you can signup [here](https://www.yoonik.me/register). To get a free trial license please e-mail us to [support@yoonik.me](mailto:support@yoonik.me).
* A [Python](https://www.python.org) developer environment.


## Setting up Okta

### Install the YooniK app integration in your Okta instance

1. Sign in to your organization's Okta Admin Console.

2. In the Admin Console, go to  **Applications** > **Applications**. Click **Browse App Catalog** and search for **YooniK**, and then click **Add**.
    
3. Enter an **Application Label** in General Settings. This is the name under which the YooniK app will appear in your Okta dashboard.
    
4. Click **Done**.

5. In the **Sign On** tab, under the **Settings** section click **Edit** and fill the **Domain** field with the domain you will be using to deploy your custom Web Application (for testing, you can use the default localhost domain: http://127.0.0.1:8080).

6. In the **Assignments** tab, assign the application to the desired users or groups.

### Configure the Web Application

1. You now need to gather the following information from the Okta Admin Console:
    
    * **Client ID** and **Client Secret** - These can be found on the **Sign On** tab of the YooniK app integration that you installed earlier in the Okta Admin Console.
        
    * **Open ID Connect URLs** - These are the **authorization_endpoint**, **token_endpoint** and **userinfo_endpoint** for your Okta domain that can be found by clicking on **OpenID Provider Metadata** link under the **Sign On** tab.
     
2. Additionally, you need to gather the **YooniK API URL** and **YooniK API key** from your YooniK account dashboard (or by contacting [support@yoonik.me](mailto:support@yoonik.me)).
    

> If you set a custom domain for this app in the **Sign On** tab in Okta Admin Console (different than http://127.0.0.1:8080), please update the **"redirect_uri"** in `config.json` accordingly.


### OIDC Well-Known Configuration

To your base Okta organization domain append `/.well-known/openid-configuration` and go to the address. This contains the OIDC needed information for the next section.

In this JSON the following keys will be important, pay attention to its values. 

```json
{
  "authorization_endpoint": "https://your-subdomain.okta.com/oauth2/v1/authorize",
  "token_endpoint": "https://your-subdomain.okta.com/oauth2/v1/token",
  "userinfo_endpoint": "https://your-subdomain.okta.com/oauth2/v1/userinfo"
}
```

## Setting up the Flask App

Open the `config.json` file.

Set the **oidc_base_url** to the OIDC common base URL (similar to `https://your-subdomain.okta.com/oauth2/v1/`).

Set **auth_url** to the part following the base URL in `authorization_endpoint`.

Set **token_url** to the part following the base URL in `token_endpoint`.

Set **userinfo_url** to the part following the base URL in `userinfo_endpoint`.

Set **token_validation_url** to `null`.

Set **client_id** and **client_secret** to its values.

Set **yoonik_authentication_api_url** and **yoonik_authentication_api_key**, if you don’t have, please contact us.

Your final result should look like this.

```json
{
  "oidc_base_url": "https://your-subdomain.okta.com/oauth2/v1/",
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


For more information, support and trial licenses please [contact us](mailto:support@yoonik.me) or join us at our [discord community](https://discord.gg/SqHVQUFNtN).
