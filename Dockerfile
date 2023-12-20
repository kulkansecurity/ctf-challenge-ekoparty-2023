FROM python:3.8-slim-buster

WORKDIR /python-docker
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app.py .
COPY templates ./templates
COPY static ./static

# required
RUN apt-get update && apt-get install -y wget unzip gnupg2

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN google-chrome --version | grep -oE "[0-9]{1,10}.[0-9]{1,10}.[0-9]{1,10}.[0-9]{1,10}" > /tmp/chromebrowser-main-version.txt 
# If the wget fails with a 404 it is likely that chrome-for-testing is behind the latest chrome version, hopefully temporarily
# In that case, refer to the latest URL and hardcode it: https://googlechromelabs.github.io/chrome-for-testing/#stable
#RUN wget -N https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/118.0.5993.70/linux64/chromedriver-linux64.zip -P ~/
RUN wget -N https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/$(cat /tmp/chromebrowser-main-version.txt)/linux64/chromedriver-linux64.zip -P ~/ 
RUN unzip ~/chromedriver-linux64.zip -d ~/ 
RUN rm ~/chromedriver-linux64.zip 
RUN mv -f ~/chromedriver-linux64 /usr/local/bin/chromedriver

EXPOSE 12000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=80"]
