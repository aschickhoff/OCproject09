<h1 align="center">OpenClassrooms Project 9</h1>
<h3 align="center">Develop a Web Application Using Django</h3>

<p align="left">This is my ninth project for OpenClassrooms where I had to create a product that enables a community of users to review books and literature on demand.</p>

## Prerequisite

- [Python3](https://www.python.org/ "Python") is installed

## Installation Steps

1. Clone the repository

```Bash
git clone https://github.com/aschickhoff/OCproject09.git
```

2. Go to your work directory
```Bash
cd OCproject09
```

## for Window
3. Create a virtual environment
```Bash
python -m venv env
```

4. Activate the virtual environment
```Bash
env\Scripts\activate
```

## for Linux
3. Create a virtual environment
```Bash
python3 -m venv env
```

4. Activate the virtual environment
```Bash
source env/bin/activate 
```

## Packages

5. Install the needed packages
```Bash
pip install -r requirements.txt
```
## Start the server

6. Launch the Django server
```Bash
python manage.py runserver
```

- Go to the landing page in your browser http://127.0.0.1:8000/

## Administration
user: admin 
password: litreview

## Registered users
user: andre, john, sarah, josie 
password: litreview



## Flake8 command
```Bash
flake8 --ignore=E501 --format=html --htmldir=f8report --exclude=env,manage.py,db.sqlite3,litreview
```