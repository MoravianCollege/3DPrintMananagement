
## Running Flask App

# Setup
* Requires a `.env` file in the root directory
    * Must contain the client id and client secret (see section Google Oauth Keys):
        * `GOOGLE_CLIENT_ID=Your_Client_Id`
        * `GOOGLE_CLIENT_SECRET=Your_Client_Secret`
* Must install necessary libraries
    * The `requirements.txt` file contains all the libraries, some with the versions used
    * Can run the command `pip3 install -r requirements.txt` to install everything in requirements.
* Before the initial run command (see next section), use command `flask init-db`
    * Generates an empty database
    * Will clear any existing database if present

# Commands in Sequence To Run
* `export FLASK_APP=.` to load the application
* `export FLASK_ENV=development` to load the environment
* `flask run --cert=adhoc` to run the application on https
    * remove the optional `--cert=adhoc` to run on http

# Google Oauth Keys
* We are using Google's Oauth 2.0 API
* Documentation on Oauth can be found here: https://developers.google.com/identity/protocols/oauth2
* To sign up for credentials
    * Head to Google Developer Console
    * Log in with your Google account
    * Go to `Credentials` on the side bar
    * Click `Create Credentials` and select Oauth client ID
    * For the moment, fill out only as much information as necessary to submit the form
    * Once complete, edit the credential
        * You can give the credential a better name
        * You must add the URI `https://3d.moravian.edu`
        * You must add the redirect URIs for:
            * `https://3d.moravian.edu` for the actual website
            * `https://127.0.0.1:5000/login/callback` for running on https on the local host
                * Google Oauth will open from an http but will not redirect to a http 
    * You can get your Client ID and Client Secret from the top right corner and place them in the `.env` (See section Setup)
    * Make sure to save the changes