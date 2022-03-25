# Recruitung_Agency
The Recruiting Agency models a company that is responsible for posting, managing opportunities, and finding candidates for those opportunities. This is a web application for the Udacity Nano Degree program, that contains Models, Endpoints, Roles, and Tests.

# Note if you're using wsl

- install postgres on wsl ubuntu [link](https://www.postgresql.org/download/linux/ubuntu/)

```
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get -y install postgresql
```

# create a virtual env

- run `pythom3 -m ven venv`
- activate env `source ./venv/bin/activate`
- run `pip install -r requirements.txt`

# How to run the project (linux or wsl)

- run `sudo apt install dos2unix`
- run `sudo dos2unix ./setup.sh` this [issue](https://stackoverflow.com/questions/39527571/are-shell-scripts-sensitive-to-encoding-and-line-endings)
- run the following command `chmod +x ./setup.sh`
- run the following command `./setup.sh`
- run `flask run --reload`

# setup database

# testing

- `source ./setup.sh`
- `python3 ./test_app.py`

# Heroku

- Assuming you have already committed all your local edits.
  `git push heroku master`
- to access the bash `heroku run bash`

# Common Issues

- if you can't connect to psql on WSL2
  `sudo /etc/init.d/postgresql start`

# Access the local postgres database

- run `sudo su postgres`
- run `psql`

# Notes

- to view a file in terminal while showing end of line characters `cat -v setup.sh`
- if heroku fails for some reason try to get the log to know what is the issue
  `heroku log --tail`

# documentation

# Greeting-backend

this is the repository for the example Recruiting Agency project

included in the repo the tokens for the different 3 users you will find them in the test_app.py

included also the a postman collection where you can use to interact with the app hosted on heroku

to access the login page you head to this [login](https://fsndtz.us.auth0.com/authorize?audience=recruit&response_type=token&client_id=2GqoWKTv8hClT5ldk2ppMLwZsisB6uIX&redirect_uri=https://127.0.0.1:8080/callback) page

## authentication

all tokens are fresh you can use them to interact with api

## endpoints

GET "/seekers"

- Fetches an json that contains an array of seekers
- Request Arguments: None
- Query Arguments:
  -page = the page number
  -limit = number of items per page
- Request Body: None
- Returns:
  - an array of jobs as show in the example response
  - status: 200

GET "/jobs"

- Fetches an json that contains an array of jobs
- Request Arguments: None
- Query Arguments:
  -page = the page number
  -limit = number of items per page
- Request Body: None
- Returns:
  - an array of jobs as show in the example response
  - status: 200
- Example Response:

```json

{
    "limit": 10,
    "jobs": [
        {

            "job": "web developer full stack",
            "field": "Software"

        }
        ...
    ],
    "next": null,
    "page": 1,
    "prev": null,
    "total": 6
}
```
