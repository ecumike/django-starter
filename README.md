# Django app starter kit
Create a new repo and select this repo as the template (or fork it).

## Included/installed Features:
- Direct LDAP connection with w3 ID/PW for signing in
- User profiling, pulls data from bluepages on user sign-in
- Debugging toolbar
- Django extensions
- "Switch user" admin feature
- Custom 403, 404, 500 error pages
- Custom error handling, including email and slack room hook notification features
- Site-wide banner notifications
- Banner notification when using production database (as opposed to local)
- Basic flexible page template
- UI framework using Tachyons, select2, tooltip and overlays
- Template helpers for preset design components; buttons, icons, header, tabs, etc
- COS (Cloud Object Storage) utility library for uploading, getting, deleting files



## Install Requirements

Python 3.7 ish +

Postgres 11 ish +



## Install

Setup a virtual environment and active it, or setup a container.

Python 3 comes with built-in `venv` so no extra virtual environment package is required.

&nbsp; &nbsp; `python3 -m venv /path/to/python-env/<name>`

...or with `virtualenv` package:

&nbsp; &nbsp; `virtualenv -p python3 /path/to/python-env/<name>`


Activate that environment:

&nbsp; &nbsp; `source /path/to/python-env/<name>/bin/activate`


Clone the repo:

&nbsp; &nbsp; `git clone git@github.ibm.com:blackops/django-starter.git`


CD to the repo root wherever you just cloned it to and install the dependencies:

&nbsp; &nbsp; `pip3 install -r requirements.txt`


### Set some local variables:

There are some local variables and settings needed for your implementation. They can either be set as environment variables, or you can add a `local_settings.py` file alongside the Django default `settings.py` file. 
It's recommended that you set these base vars as environment variables so you only do this once and each Django app will use these same settings. In your `local_settings.py` file you can add app-specific local settings(If you like to add base settings you can use base_settings.py along side the settings file).

You only need to replace the two `___` with your local Postgres user ID and PW. 
`SCRIPT_NAME` is intentionally blank.


```
    export DJANGO_DB_USER=____
    export DJANGO_DB_PASSWORD=____
    export DJANGO_DEBUG_FLAG=True
    export DJANGO_FORCE_SCRIPT_NAME=
```
    
For the initial setup, create a postgresql database called `myproject`. When you rename your app, you'll change this to your project name.
(Ensure your user account can write to the database)


Have Django setup the database according to the models. From the repo root:

&nbsp; &nbsp; `./manage.py migrate`

Create a superuser (follow the prompts, you can leave email blank):

&nbsp; &nbsp; `./manage.py createsuperuser`



## Running and developing

Every time you want to start the app, there are 3 steps:
1. Ensure you are in your environment you created above.
2. CD to the local repo root.
3. Start up Django.
 
 
Detailed steps:

1. Ensure you have the environment activated:

&nbsp; &nbsp; `source /path/to/env/<name>/bin/activate`

2. CD to the repo root:

&nbsp; &nbsp; `cd /some/path/to/repo`

3. Start the Django app:

&nbsp; &nbsp; `./manage.py runserver`

Now you can open your browser to http://localhost:8000/myapp/  and you should see it.

Make your changes and simply reload your browser page to see them.


### Pro tip
Create a script alias to do all this for you. Add this line in your `.bash_profile` file:

`alias startmyapp='source /path/to/this-app-env/bin/activate && cd /some/path/to/repo/ && ./manage.py runserver'`

 
## Using for your own app
Once you have this starter up and running you'll want to change the name of the project and app to what you want your real name to be.

1. Replace every instance of `myproject` in all files. Do a global search and replace in the repo and replace `myproject` with your project short name (no spaces or dashes).
2. Change the `myproject` directory in the root to your project short name.
3. Replace every instance of `myapp` in all files. Do a global search and replace in the repo and replace `myapp` with your app's short name (no spaces or dashes).
4. Change the `myapp` directory in the root to your app's short name.
5. Change the `myapp` directory in the `templates` directory to your app's short name.
6. Create your real database with the same name as your project (set in step 1) or rename the starter one: `ALTER DATABASE myproject RENAME TO ____;`


## To have 404 and 500 error message send alerts to a slack channel.
Set this ENV VAR with the appropriate channel inbound hook URL

`SLACK_ALERT_URL = 'https://hooks.slack.com/services/xxxxx/xxxxx/xxxxxxxxxxxxxxxxxxx'`

## Email is setup via settings.EMAIL_HOST. It uses the IBM mail relay. 


## To use Cloud Object Storage, set these ENV VARS with your COS account info.
```
COS_API_KEY_ID = 'xxxxxxxxxxxxxx'
COS_RESOURCE_CRN = 'crn:xxxxxxxxxxxxxx'
COS_AUTH_ENDPOINT = 'https://iam.cloud.ibm.com/identity/token'
COS_ENDPOINT = 'https://xxxxxxxxxxxxxx'
COS_BUCKET_LOCATION = 'us-south-standard'
COS_BUCKET_NAME = 'xxxxxxxxxx'
```

## To use SSO
IBM SSO:  https://ies-provisioner.prod.identity-services.intranet.ibm.com/tools/sso/
Django OIDC module in use:  https://mozilla-django-oidc.readthedocs.io/en/stable/

There are a lot of little settings needed for SSO to work. I will be posting a separate doc. for that.

## Documentation
Django Admin Docs is setup. It will automatically read your models, doc strings, relationships, methods and arguments, etc and provide detailed reading, along with all the Django built-in template tags and features. Admin documentation link is in the top right links on the built-in Django admin.


## Coding style guidelines
 
We follow the basic Django and Python coding principles and styles:  
https://docs.djangoproject.com/en/2.2/misc/design-philosophies/  
https://docs.djangoproject.com/en/2.2/internals/contributing/writing-code/coding-style/  

→  [Python and Django packages we use](https://github.ibm.com/blackops/tech-docs/wiki/Python-and-Django-packages)  

 
