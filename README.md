## KU Polls: Online Survey Questions 

An application to conduct online polls and surveys based
on the [Django Tutorial project](TODO-write-URL-of-the-django-tutorial-here), with
additional features.

This app was created as part of the [Individual Software Process](
https://cpske.github.io/ISP) course at [Kasetsart University](https://www.ku.ac.th).

## Installation and Running the Application

1. Clone this project repository to your machine.

`git clone https://github.com/premepreme/ku-polls.git`

2. Get into the directory of this repository.

`cd ku-polls`

3. Create a virtual environment.

`python -m venv venv`

4. Install all required packages. pip install -r requirements.txt Create .env file in ku-polls

`
SECRET_KEY = 'django-insecure-rnug$7zncble0(+xdf%c-%%*y*dm=616&c)epl+m!*#a8p9@!0'
DEBUG = True
TIME_ZONE = UTC
`

5. Run this command to migrate the database.

`python manage.py migrate`

6. Start running the server by this command.

`python manage.py runserver`

## Project Documents

All project documents are in the [Project Wiki](../../wiki/Home).

- [Iteration 1 Plan](../../wiki/Iteration-1-Plan)
- [Iteration 2 Plan](../../wiki/Iteration-2-Plan)
- [Vision and Scope](../../wiki/Vision-and-Scope)
- [Project Plan](../../wiki/Project-Plan)
- [Requirements](../../wiki/Requirements)
