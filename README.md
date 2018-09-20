# bitsat
Do you have a question or a doubt about bitsat or BITS in general? This website will help solve your problems.
This is a forum made using django to help solve all your problems.

FOR DEVELOPERS :

**This requires the latest version of Django or version greater than 2.0**
**It's made using python 3.**
**It requires an internet connection to run locally as bootstrap CDN is linked in the templates**

## Getting started
You'll need to install the following:
-pip
-python

To download this repo:
```git
    git clone https://github.com/palindrome69/bitsat.git
```

You'll require the following libraries:
-django
-django-bootstrap4
-maybe some others I don't remember. install them if you get an error :3

Move to repo's directory using the following command.
```bash
    cd bitsat
 ```
 ## DEPLOYING LOCALLY
 
 To deploy this site locally run the following command while in directory:

 ```python
python manage.py runserver
```
you should see a message like:
```bash
Performing system checks...

System check identified no issues (0 silenced).
September 19, 2018 - 22:05:24
Django version 2.0.3, using settings 'bitsat.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```
go to the url mentioned and append 'home' to it .It should look like this :
http://127.0.0.1:8000/home/

## Creating Superuser

to create a superuser to acces the admin site:
run the following command
```python
python manage.py createsuperuser
```
then do as prompted.

## USAGE
Go to the site home which was demonstrated earlier
Then register a new user and log in
## FEATURES
-You can ask questions
-Post answers
-Upvote or downvote a question
-Delete an answer or a question (should be your own)
-You also can edit your profile and change password
-You can view other users' profile and their questions
-You can follow a question to get notifications when someone posts an answer to it

## Admin Site
To access admin you'll need to create a superuser
Steps are given above on how to create a superuser
Then run the runserver command and instead of appending 'home'
to the end add 'admin/' to it.
A login page will appear log in to it user your superuser credentials
and you'll go to the admin page.

## AUTHOR
-  https://github.com/palindrome69/
