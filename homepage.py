# Python standard libraries
import json
import os
import sqlite3

# Third party libraries

from flask import Flask, redirect, request, url_for, render_template, session, Blueprint, jsonify

from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests

from flask_sqlalchemy import SQLAlchemy

# Internal imports
from .DBTableCreation import Users
from . import db, login_manager
from .ultimaker import Ultimaker, PrintJob, PrintJobState, PrintJobResult

bp = Blueprint("homepage2", __name__, url_prefix="")

# Configuration
GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)

# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(user_id) if user_id is not None else None


@bp.route("/")
def index():
    if current_user.is_authenticated:
        return render_template('form.html')
    else:
        return render_template('welcome.html')


@bp.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@bp.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    user = Users.query.filter_by(email=users_email).first()

    # Doesn't exist? Add to database
    if not user:
        #User.create(unique_id, users_name, users_email, picture)
        user = Users(name=users_name, email=users_email)
        db.session.add(user)
        db.session.commit()

    # Begin user session by logging the user in
    login_user(user)

    # Send user back to homepage
    return redirect(url_for("index"))


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@bp.route("/form")
@login_required
def req_form():
    return redirect(url_for("index"))


@bp.route("/status")
@login_required
def printer_status():
    # Xerox request state
    try:
        Xerox = PrintJob(Ultimaker("172.31.228.191", None, None))
        Xerox_status = Xerox.state
        Xerox_name = Xerox.name
        Xerox_finish = get_remaining_time(Xerox)
       
    except Exception as e:
        # If Printer is not doing a job
        if str(e) == "'Not found'":
            Xerox_status = PrintJobState.NO_JOB 
        
        # Printer is off, UNKNOWN = OFF
        else:
            Xerox_status = PrintJobState.UNKNOWN

        Xerox_name = ""
        Xerox_finish = ""
            
    # Gutenberg request state
    try:
        Gutenberg = PrintJob(Ultimaker("172.31.228.190", None, None))
        Gutenberg_status = Gutenberg.state
        Gutenberg_name = Gutenberg.name
        Gutenberg_finish = get_remaining_time(Gutenberg)
        
       
    except Exception as e:
        # If Printer is not doing a job
        if str(e) == "'Not found'":
            Gutenberg_status = PrintJobState.NO_JOB

        # Printer is off, UNKNOWN = OFF
        else:
            Gutenberg_status = PrintJobState.UNKNOWN
        
        Gutenberg_name = ""
        Gutenberg_finish = ""
 
    Xerox_status, Gutenberg_status = get_status_string(Xerox_status, Gutenberg_status)
    
    return render_template('status.html',
                           X_status=Xerox_status,
                           G_status=Gutenberg_status,
                           X_name=Xerox_name,
                           G_name=Gutenberg_name,
                           X_finish=Xerox_finish,
                           G_finish=Gutenberg_finish)


@bp.route("/queue")
@login_required
def queue():
    return render_template('queue.html')


@bp.route("/members")
@login_required
def members():
    return render_template('members.html')


@bp.route("/success", methods=["POST"])
@login_required
def success():
    # Get results from request form
    results = request.form
    
    # Check if the user actually included a print
    if not request_has_printjob(results):   
        return redirect(url_for("failure"))

    # Print was given
    return render_template('success.html')


@bp.route("/error-no-print-attached")
@login_required
def failure():
    return render_template('failure.html')


@bp.route("/pause-printer/Xerox", methods=["GET"])
@login_required
def pause_xerox():
    Xerox = PrintJob(Ultimaker("172.31.228.191", None, None))
    Xerox.pause()
    
    return jsonify({'success': 'true'})

@bp.route("/pause-printer/Gutenberg", methods=["GET"])
@login_required
def pause_gutenberg():
    Gutenberg = PrintJob(Ultimaker("172.31.228.190", None, None))
    Gutenberg.pause()

    return jsonify({'success': 'true'})


@bp.route("/resume-printer/Xerox", methods=["GET"])
@login_required
def resume_xerox():
    Xerox = PrintJob(Ultimaker("172.31.228.191", None, None))
    Xerox.resume()
    
    return jsonify({'success': 'true'})


@bp.route("/resume-printer/Gutenberg", methods=["GET"])
@login_required
def resume_gutenberg():
    Gutenberg = PrintJob(Ultimaker("172.31.228.190", None, None))
    Gutenberg.resume()

    return jsonify({'success': 'true'})


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


def request_has_printjob(results):
    # Check if has link
    if results.get("link") == '':
        # Check if has file
        if results.get("files") == '':
            # No print was given
            return False
        # Check the file type
        if check_file_type_not_allowed(results.get("files")):
            # File is neither an stl or zip file
            return False

    return True


def check_file_type_not_allowed(file_name):
    # If the file is not a stl file
    if ".stl" not in file_name:
        # If the file is not a zip file
        if ".zip" not in file_name:
            return True
    
    # The file is either an stl or a zip
    return False


def get_status_string(Xerox, Gutenberg):
    Xerox_status = get_status_message(Xerox)
    Gutenberg_status = get_status_message(Gutenberg)
    return (Xerox_status, Gutenberg_status)


def get_status_message(status):
    if status == PrintJobState.NO_JOB:
        return "IDLE"
    elif status == PrintJobState.PRINTING:
        return "PRINTING"
    elif status == PrintJobState.PAUSING:
        return "PAUSING PRINT"
    elif status == PrintJobState.PAUSED:
        return "PAUSED"
    elif status == PrintJobState.RESUMING:
        return "RESUMING PRINT"
    elif status == PrintJobState.PRE_PRINT:
        return "PREPARING"
    elif status == PrintJobState.POST_PRINT:
        return "FINISHED"
    elif status == PrintJobState.WAIT_CLEANUP:
        return "WAITING FOR CLEANUP"
    elif status == PrintJobState.WAIT_USER_ACTION:
        return "WAITING FOR RESET"
    else:
        return "OFF"


def get_remaining_time(print_job):
    return ("Remaining time for print: " +
            str(print_job.time_total - print_job.time_elapsed))


if __name__ == "__main__":
    # Run HTTPS
    bp.run(ssl_context="adhoc")
