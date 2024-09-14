# Installation

1. Clone this project repository to your machine.

  `git clone https://github.com/premepreme/ku-polls.git`

2. Get into the directory of this repository.

`cd ku-polls`

3. Create a virtual environment.

`python -m venv venv`

4. Activate the virtual environment.

`. env/bin/activate`

5. Install all required packages. `pip install -r requirements.txt` Create .env file in ku-polls

```
SECRET_KEY = 'django-insecure-rnug$7zncble0(+xdf%c-%%*y*dm=616&c)epl+m!*#a8p9@!0'
DEBUG = True
TIME_ZONE = UTC
```

6. Run this command to migrate the database.

```
python manage.py migrate
python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
```

7. Start running the server by this command.

`python manage.py runserver`
