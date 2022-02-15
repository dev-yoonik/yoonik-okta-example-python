# Okta + YooniK App Configuration guide

## Overview

This integration guide configures a custom Web Application using the Okta Sign-in Widget and YooniK Face Authentication APIs to demonstrate how to add a second-factor authentication to Okta login flow, enhancing security and privacy while providing a seamless user experience.

## Contents

* Supported features
* Requirements
* Configuration steps
* Notes

## Supported features

* Service Provider (SP)-Initiated Authentication (SSO) Flow - This authentication flow occurs when the user attempts to log in from YooniK application.

## Requirements

This app integration has the following requirements:

* An Okta Account.
* An YooniK account. If you do not already have one, you can signup [here](https://www.yoonik.me/register). To get a free trial license please e-mail us to [support@yoonik.me](mailto:support@yoonik.me).
* A [Python](https://www.python.org) developer environment.

## Configuration steps

### Install the YooniK app integration in your Okta instance

1. Sign in to your organization's Okta Admin Console.
2. In the Admin Console, go to  **Applications** > **Applications**.
3. Click **Browse App Catalog** and search for **YooniK**, and then click **Add**.
4. Enter an **Application Label** in General Settings. This is the name under which the YooniK app will appear in your Okta dashboard.
5. Click **Done**.
6. In the **Sign On** tab, under the **Settings** section click **Edit** and fill the **Domain** field with the domain you will be using to deploy your custom Web Application (for testing, you can use the default localhost domain: http://127.0.0.1:8080).
7. In the **Assignments** tab, assign the application to the desired users or groups.

### Configure the Web Application

The following steps cover the configuration and deployment of a sample application that enables you to test your YooniK and Okta integration.

1. Clone the example application repository from [GitHub](https://github.com/dev-yoonik/yoonik-okta-example-python) to a local folder on your system.
2. Open a terminal and change to the base directory where you cloned the repository.
3. Then install dependencies: `$ pip install -r requirements.txt`.
4. Copy the `client_secrets.json.dist` to `client_secrets.json`: `$ cp client_secrets.json.dist client_secrets.json`.
5. You now need to gather the following information from the Okta Admin Console:
   * **Client ID** and **Client Secret** - These can be found on the **Sign On** tab of the YooniK app integration that you installed earlier in the Okta Admin Console.
   * **Open ID Connect URLs** - These are the **authorization_endpoint**, **token_endpoint** and **userinfo_endpoint** for your Okta domain that can be found by clicking on **OpenID Provider Metadata** link under the **Sign On** tab.
6. Additionally, you need to gather the **YooniK API URL** and **YooniK API key** from your YooniK account dashboard (or by contacting [support@yoonik.me](mailto:support@yoonik.me)).
7. Fill in the information that you gathered in the `client_secrets.json` file.

> If you set a custom domain for this app in the **Sign On** tab in Okta Admin Console (different than http://127.0.0.1:8080), please update the **"redirect_uri"** in `client_secrets.json` accordingly.

You are now ready to start testing your new app with Okta login and YooniK Face Authentication as a second-factor!

### Test the Web Application

1. Launch the app server from a terminal window: `$ python main.py`.
2. Now navigate to [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser. If you see a home page that prompts you to log in, then things are working!
3. Clicking the **Log in** button will redirect you to the Okta hosted sign-in page. Enter the credentials of a valid Okta account and proceed.
4. Then a new screen will be displayed to perform the second-factor authentication with YooniK. Just look at your webcam and click the **take selfie** button!
5. After the face authentication, your are logged in to the application!

## Notes

### Additional Resources

* [Okta Hosted Login + YooniK Face Authentication](https://github.com/dev-yoonik/yoonik-okta-example-python) example on Github.
* Subscribe YooniK Face Authentication [here](https://www.yoonik.me/pricing).

### Contact & Support

For more information, support and trial licenses please [contact us](mailto:support@yoonik.me) or join us at our [discord community](https://discord.gg/SqHVQUFNtN).
