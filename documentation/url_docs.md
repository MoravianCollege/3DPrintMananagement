# /
* If user has not logged in
    * Displays a welcome page
    * Button to login redirect to the `/login` url
* If user is logged in
    * Sidenave bar is displayed for user to jump around endpoints
    * Displays a request form page
    * Submission button redirects to the `/success` url

# /login
* Makes the call to Google Oauth
* Brings up Google Oauth login page
* Upon logging into an account
    * If the account is not a moravian account, gives the default Oauth error for unautherized access
    * If the account is a moravian account, makes call to `/login/callback` url

# /login/callback
* Gets the information from Oauth on the user
* Adds the user to the `User` database if they are not already in the database
* Logs the user into flask_login and adds the information to the flask-login global object `current_user`
* Redirects the logged in user to `/` url

# /logout
* Logs the user out of flask-login
* Redirects the now logged out user to the `/` url

# /form
* Redirects to the `/` url

# /status
* Makes contact with the Ultimakers
    * Attempts to get status, current print name, total time for the print, and time elapsed for the print
    * Both `NO_JOB` and `UNKNOWN` (off) status throw exceptions
        * `NO_JOB` exception will be `'Not found'`
* Sends data to the html to display
    * Page auto refreshes every 5s
        * To change refresh rate, change the number in the meta tag for content to the desired amount of seconds
```
<meta http-equiv="refresh" content=NUMBER_AS_SECONDS>
```

# /queue
* Not yet Implemented
    * Will display a list of prints queued

# /members
* Not yet Implemented
    * Will display a list of the members with contact information (email)
* Admin can use a button to move to the `/admin-check` url

# /success
* Not fully implemented
    * Needs to save results to a database(s)
* Checks if the form submitted contains either a thingiverse link, a `.stl` file, or a `.zip` file
* If the form has one of the three, displays a success page
* If the form has none, redirects to the `/error-no-print-attached` url

# /error-no-print-attached
* Displays a print failed page
* Informs user with a generic failure message that the submission was missing a pring being attached

# /pause-printer/Xerox
* Checks if user has access
* If user has access
    * Sends a pause print command to the Ultimaker Xerox
    * Returns a json value of `true` to the key `success`
* If the user does not have access
    * Returns a json value of `false` to the key `success`

# /resume-printer/Xerox
* Checks if user has access
* If user has access
    * Sends a resume print command to the Ultimaker Xerox
    * Returns a json value of `true` to the key `success`
* If the user does not have access
    * Returns a json value of `false` to the key `success`

# /pause-printer/Gutenberg
* Checks if user has access
* If user has access
    * Sends a pause print command to the Ultimaker Gutenberg
    * Returns a json value of `true` to the key `success`
* If the user does not have access
    * Returns a json value of `false` to the key `success`

# /resume-printer/Gutenberg
* Checks if user has access
* If user has access
    * Sends a resume print command to the Ultimaker Gutenberg
    * Returns a json value of `true` to the key `success`
* If the user does not have access
    * Returns a json value of `false` to the key `success`

# /admin-check
* If the user is not an admin, redirects to the `/` url
* If the user is an admin
    * Gets a form to fill out with different access switches
    * Email of the worker is required for all access switches
    * Can use multiple access switches per submission
    * Redirects to the `/` url

# /manage-members
* Temporary manual access switcher
* Checks each field in the form
    * If the field is not empty, will attempt manipulate the database
    * If the databse gets manipulated, adds the email (and possibly other info) as a value to a dictionary key of the action
        * Activating a worker's access would add {'activate': email} to the dictionary
    * Redirects to a page with the json.dumps of the dictionary of actions occured
* If a non admin user attempts to access this page, redirects to the `/` url