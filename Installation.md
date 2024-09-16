# Installation

1. Clone this project repository to your machine.

  `git clone https://github.com/NapatrSaengthongsakullert/ku-polls.git`

2. Get into the directory of this repository.

`cd ku-polls`

3. Create a virtual environment.

`python -m venv venv`

4. Activate the virtual environment.

```
on Windows:
.\env\scripts\activate

on macOS/linux:
.env/bin/activate
```

5. Install all required packages.

`pip install -r requirements.txt`

6. Create .env file in ku-polls and copy this code to the file or copy from sample.env
```
SECRET_KEY = 'django-insecure-rnug$7zncble0(+xdf%c-%%*y*dm=616&c)epl+m!*#a8p9@!0'
DEBUG = True
TIME_ZONE = Asia/Bangkok
ALLOWED_HOSTS = localhost, 127.0.0.1
```

6. Migrate the database and import the poll data

```
python manage.py migrate
python manage.py loaddata data/polls-v4.json data/votes-v4.json data/users.json
```

7. Start running the server by this command.

`python manage.py runserver`
