# Argyle Challenge Upwork Scanner

## **Running as local environment API**


#### **credential variables**
Rename _.credentials-sample.json_ to _.credentials.json_, then fill all necessary(login, password) values:
```json
{
    "login": "username",
    "password": "password",
    "secret_answer":"secret_answer",
    "auth_secret_key":"auth_secret_key"
}
```


#### **Virtual environment**
Create virtual environment with python 3.10
```console
virtualenv env -p 3.10
```
Activate environment.
```console
source env/bin/activate
```



#### **Installing dependencies**
Using pip:
```console
pip install -r requirements.txt
```
or, using poetry to manage dependencies:
```console
pip install poetry
poetry install --no-interaction
```


#### **Chrome driver**
Download [Chrome Driver](https://chromedriver.chromium.org/downloads) and include its location in your system `PATH` environment variable.
Download, install or update your Google Chrome or Chromium browser, based on Chrome Driver' support version.


#### **Running the application**
```console
uvicorn main:app
```
#### **Access** 
[Work listings](http://localhost:8000/works) for listing of works.
[User's profile](http://localhost:8000/profile) for the user's profile.


#### **Usage**
Generate a json output:
1. **profile**: `Scraping().get_profile_content()`.
2. **works**: `Scraping().get_portal_content()`.

All methods saves a individual json file at **output** path.

## Models

**Work**

```
title: str
url: str
description: str
tags: List[str]
location: str
client_spendings: str
payment_status: str
rating: str
job_type: str
tier: str
date: datetime
```

**Profile**

```
id: int
account: str
employer: str
created_at: datetime
updated_at: Optional[datetime]
first_name: str
last_name: str
full_name: str
email: str
phone_number: int
birth_date: Optional[datetime]
picture_url: str
address: Address
ssn: Optional[int]
marital_status: Optional[str]
gender: Optional[str]
metadata: dict = {}
```
## Running app on docker
#### **credential variables**
Rename _.credentials-sample.json_ to _.credentials.json_, then fill all necessary(login, password) values:
```json
{
    "login": "username",
    "password": "password",
    "secret_answer":"secret_answer",
    "auth_secret_key":"auth_secret_key"
}
```
Build the application's image.
```console
docker build -t argyle_upwork_scanner .
```
Run application's image.
```console
docker run -d --name scraper_container -p 8000:8000 argyle_upwork_scanner
```
#### **Access** 
[Work listings](http://localhost:8000/works) for listing of works.
[User's profile](http://localhost:8000/profile) for the user's profile.

