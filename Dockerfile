FROM python:3.9

# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Install google-chrome-stables
RUN apt-get install -y google-chrome-stable

# Installing Unzip
RUN apt-get install -yqq unzip

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN wget -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver_linux64.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99

RUN pip install --upgrade pip
#
WORKDIR /code
#
COPY ./requirements.txt /code/requirements.txt
COPY ./models /code/models
COPY ./scraper /code/scraper
COPY ./main.py /code/main.py
COPY ./wsgi.py /code/wsgi.py
COPY ./README.md /code/README.md
COPY ./.credentials.json /code/.credentials.json

#
RUN mkdir /code/output
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]






