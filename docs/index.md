# Okta + YooniK App Configuration guide

## Overview

This integration guide configures a custom Web Application using the Okta Sign-in Widget and YooniK Face Authentication APIs to demonstrate how to add a second-factor authentication to Okta login flow, enhancing security and privacy while providing a seamless user experience.

## Prerequisites

This app integration has the following requirements:

*   An Okta Developer Account, you can sign up for one at [https://developer.okta.com/signup/](https://developer.okta.com/signup/) .
    
*   An YooniK account. If you do not already have one, you can signup [here](https://www.yoonik.me/register). To get a free trial license please e-mail us to [support@yoonik.me](mailto:support@yoonik.me).
    
*   A [Python](https://www.python.org) developer environment.
    

## Procedure

### Create an OpenID Connect app integration

1.  Sign in to your Okta developer account as a user with administrative privileges.
    
2.  In the Admin Console, go to  **Applications** > **Applications**.
    
3.  Click **Create App Integration**.
    
4.  On the Create a new app integration page, select **OpenID Connect** in the **Sign-in method** section.
    
5.  Choose **Web Application** as the **Application type** for your integration. Click **Next**.
    
6.  In **General Settings**, enter a name for your integration and (optionally) upload a logo.
    
7.  You can set the **Sign-in redirect URI to**  `http://127.0.0.1:8080/authorization-code/callback` and the **Sign-out redirect URI** to `http://127.0.0.1:8080`.
    
8.  Click **Save**.
    
9.  On the **General** tab for the app integration, confirm that the **Authorization Code** is selected in the **Grant types** section.
    
10.  In the **Assignments** tab for the app integration, assign the application to the desired users or groups.
    

### Configure the Web Application

The following steps cover the configuration and deployment of a sample application that enables you to test your YooniK and Okta integration.

1.  Clone the example application repository from [GitHub](https://github.com/dev-yoonik/yoonik-okta-example-python) to a local folder on your system.
    
2.  Open a terminal and change to the base directory where you cloned the repository.
    
3.  Then install dependencies: `$ pip install -r requirements.txt`.
    
4.  Copy the `client_secrets.json.dist` to `client_secrets.json`: `$ cp client_secrets.json.dist client_secrets.json`
    
5.  You now need to gather the following information from the Okta Developer Console:
    
    *   **Client ID** and **Client Secret** - These can be found on the **General** tab of the app integration that you created earlier in the Okta Developer Console.
        
    *   **Issuer** - This is the URL of the authorization server that will perform authentication. All Developer Accounts have a "default" authorization server. The issuer is a combination of your Org URL (found in the upper right of the console home page) and `/oauth2/default`. For example, `https://dev-1234.oktapreview.com/oauth2/default`.
        
6.  Additionally, you need to gather the **YooniK API URL** and **YooniK API key** from your YooniK account dashboard (or by contacting [support@yoonik.me](mailto:support@yoonik.me)).
    
7.  Fill in the information that you gathered in the `client_secrets.json` file.
    

You are now ready to start testing your new app with Okta login and YooniK Face Authentication as a second-factor!

### Test the Web Application

1.  Launch the app server from a terminal window: `$ python main.py`.
    
2.  Now navigate to [http://127.0.0.1:8080](http://127.0.0.1:8080) in your browser. If you see a home page that prompts you to log in, then things are working!
    
3.  Clicking the **Log in** button will redirect you to the Okta hosted sign-in page. Enter the credentials of a valid Okta account and proceed.
    
4.  Then a new screen will be displayed to perform the second-factor authentication with YooniK. Just look at your webcam and click the **take selfie** button!
    
5.  After the face authentication, your are logged in to the application!
    

## Additional Resources


*   [Okta Hosted Login + YooniK Face Authentication](https://github.com/dev-yoonik/yoonik-okta-example-python) example on Github.
    
*   Subscribe YooniK Face Authentication [here](https://www.yoonik.me/pricing).
    

## Contact & Support


For more information, support and trial licenses please [contact us](mailto:support@yoonik.me) or join us at our [discord community](https://discord.gg/SqHVQUFNtN).
