# Cyber Security Base 2022 - Project 1
This is the repository for [Project 1](https://cybersecuritybase.mooc.fi/module-3.1) of the course series [Cyber Security Base 2022](https://cybersecuritybase.mooc.fi/).

The project has a simple messaging application (called 'Poster') where users can send messages to each other. The application code is largely based on the exercise template of the exercise ['Cookie heist'](https://cybersecuritybase.mooc.fi/module-2.3/1-security#programming-exercise-cookie-heist) from part III of the course 'Securing Software', with own modifications and additions.

The application contains serious security flaws and therefore it is not advisable to use it in production.

## Requirements
Requires installing Python 3 to run.

## Running locally
After cloning the repository, go to the 'project_1' folder ('project_1' root, not repository root) where you should see the file 'manage.py'. You can start the application server by running the 'manage.py' file with python (command ```python manage.py runserver``` or ```python3 manage.py runserver``` depending on your OS). Once the server is started go to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in browser.
