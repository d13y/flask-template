# Flask App Template
A repository for the development of a Python web app using Flask infrastructure.


## Overview
This repository provides the following:
* A template html file for quick adoption and easy editing for all - new and existing - web pages.
* The ability for users to create accounts, login, and update their details.

*Note that this repository does not currently provide details on how to deploy/publish the app.*


## Configuration
This app uses [conda](https://docs.conda.io/en/latest/) for package management.

### App
* The [config.py]((https://github.com/d13y/flask-template/blob/master/flaskapp/config.py)) file is used set required app parameters. Parameters include: secret key; SQL database info; and mail credentials.
* Parameters are set for local usage. These can be set - and stored - in system environment variables. Tutorials: [Windows](https://www.youtube.com/watch?v=IolxqkL7cD8); and [Mac](https://www.youtube.com/watch?v=5iWhQWVXosU).

### Web Design
* Code is written in `html` and relies on [Bootstrap](https://getbootstrap.com/) templates.
* Note that `{% %}` is used to specify code that is to be run.
* [layout.html](https://github.com/d13y/flask-template/blob/master/flaskapp/templates/layout.html) file contains the basic webpage structure that is adopted by all other pages.
* Usage works as follows:
  * `{% extends "layout.html" %}` imports the [layout.html](https://github.com/d13y/flask-template/blob/master/flaskapp/templates/layout.html) webpage structure to other webpages.
  * `{% block title %} {{ title }} {% endblock title %}` sets the specific displayed page name to the title defined in the respective `/routes.py` function.
  * `{% block content %} {% endblock content %}` encompasses any page specific html or content that is to be displayed.
  

## Account Management
### User Database
* An empty user database - named [site.db](https://github.com/d13y/flask-template/blob/master/flaskapp/site.db) - has been created which stores all data related to user accounts.
* This database is used for all user account management actions.

### Registration
* Registration requires an email address and username that have not already been taken, and a password. 
* Once registered, an authentication email is sent to confirm the user has access to the registered email before the account can be used. Following the link in the email verifies the account.

### Login
* Login requires an authenticated account.
* Login requires an account's email address and password.

### Update Details
* Several account details can be updated: username, email address, and profile picture.
* Username can be set to anything not already taken.
* Profile picture changes will save a resized - and randomly named - copy of the image in the [profile_pics](https://github.com/d13y/flask-template/tree/master/flaskapp/static/profile_pics) folder, and delete the old image (unless the old image was the default picture).
* Email address changes require an additional authentication step to verify that the user has access to the new email address.

### Reset Password
* Password resets can be done via email.
* Requests to reset passwords send an email to the registered email address. Following the link in the email enables the user to reset their account password.


## Folder Structure
### [flask-template](https://github.com/d13y/flask-template)
* Contains all other folders specific to the app
* Contains several other files:
  * [.gitattributes](https://github.com/d13y/flask-template/blob/master/.gitattributes) - generic default file for text readers.
  * [.gitignore](https://github.com/d13y/flask-template/blob/master/.gitignore) - list of files to ignore (default setup, for use with PyCharm, plus project specific ignores).
  * [environment.yml](https://github.com/d13y/flask-template/blob/master/environment.yml) - list of all packages used by project.
  * [LICENSE](https://github.com/d13y/flask-template/blob/master/LICENSE) - GNU General Public License v3.
  * [run.py](https://github.com/d13y/flask-template/blob/master/run.py) - runs app.
  * [README.md](https://github.com/d13y/flask-template/blob/master/README.md) - this file.
  
### [flaskapp](https://github.com/d13y/flask-template/tree/master/flaskapp)
* The central source for all code directly related to running the app.
* Contains several subfolders:
  * [main](https://github.com/d13y/flask-template/blob/master/flaskapp/main) - folder for handling pages not related to users.
  * [static](https://github.com/d13y/flask-template/blob/master/flaskapp/static) - folder for handling user profile pictures and css styles.
  * [templates](https://github.com/d13y/flask-template/blob/master/flaskapp/templates) - folder for handling all webpage templates
  * [users](https://github.com/d13y/flask-template/blob/master/flaskapp/users) - folder for handling all user-related code

* Contains several other files:
  * [\_\_init__.py](https://github.com/d13y/flask-template/blob/master/flaskapp/__init__.py) - required to identify folder as a module package.
  * [config.py](https://github.com/d13y/flask-template/blob/master/flaskapp/config.py) - contains configuration parameters required for app functionality.
  * [models.py](https://github.com/d13y/flask-template/blob/master/flaskapp/models.py) - contains `User` database structure for site.db, validation for email authentication and password reset, and loader manager for user login.
  * [site.db](https://github.com/d13y/flask-template/blob/master/flaskapp/site.db) - contains database containing all user data.
  
### [main](https://github.com/d13y/flask-template/blob/master/flaskapp/main)
* Folder for handling code not related to users.
* Contains several other files:  
  * [\_\_init__.py](https://github.com/d13y/flask-template/blob/master/flaskapp/main/__init__.py) - required to identify folder as a module package.
  * [routes.py](https://github.com/d13y/flask-template/blob/master/flaskapp/main/routes.py) - contains routes for webpages.
  
### [static](https://github.com/d13y/flask-template/tree/master/flaskapp/static)
* Folder for handling user profile pictures and css styles.
* Contains a [profile_pics](https://github.com/d13y/flask-template/tree/master/flaskapp/static/profile_pics) subfolder which includes a default profile called `default.jpg`, plus any active user-uploaded profile pictures.
* Contains the [main.css](https://github.com/d13y/flask-template/blob/master/flaskapp/static/main.css) file, which includes the formatting for core webpage design elements.

### [templates](https://github.com/d13y/flask-template/tree/master/flaskapp/templates)
* Folder contains all webpage html templates accessed by any `/routes.py` file.
* [layout.html](https://github.com/d13y/flask-template/blob/master/flaskapp/templates/layout.html) file contains the basic webpage structure that is adopted by all other pages.

### [users](https://github.com/d13y/flask-template/tree/master/flaskapp/users)
* Folder for handling code not related to users.
* Contains several other files:
  * [\_\_init__.py](https://github.com/d13y/flask-template/blob/master/flaskapp/users/__init__.py) - required to identify folder as a module package.
  * [routes.py](https://github.com/d13y/flask-template/blob/master/flaskapp/users/routes.py) - contains routes for user related webpages (e.g. login page)
  * [forms.py](https://github.com/d13y/flask-template/blob/master/flaskapp/users/forms.py) - contains all user forms (e.g. registration, update account details...).
  * [utils.py](https://github.com/d13y/flask-template/blob/master/flaskapp/users/utils.py) - contains several user specific functions (e.g. send authentication emails).
  
  
## Credit
- This template was heavily influenced by [Corey Schafer](https://www.youtube.com/user/schafer5) and his [Python Flask Tutorial](https://www.youtube.com/playlist?list=PL-osiE80TeTs4UjLw5MM6OjgkjFeUxCYH) series on YouTube.
- This template uses [Bootstrap](https://getbootstrap.com/) for the webpage layout and design.
