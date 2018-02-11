FROM ubuntu:latest


# install standard packages
RUN apt-get update && apt-get install -y \
    bsdtar \
    build-essential \
    curl \
    dialog \
    git \
    nano \
    net-tools \
    tar \
    unzip \
    wget \
    xvfb


# install python dependencies
RUN apt-get install -y python python-dev python-distribute python-pip


# install python libraries from requirements.txt
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt


# install chromedriver for selenium headless mode
#RUN PLATFORM=linux64
#RUN VERSION=$(curl http://chromedriver.storage.googleapis.com/LATEST_RELEASE)
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN dpkg -i google-chrome-stable_current_amd64.deb; apt-get -fy install
#RUN wget http://chromedriver.storage.googleapis.com/2.35/chromedriver_linux64.zip
#RUN unzip chromedriver_linux64.zip
#RUN mv chromedriver /usr/bin

# install geckodriver and firefox
#RUN GECKODRIVER_VERSION=`curl https://github.com/mozilla/geckodriver/releases/latest | grep -Po 'v[0-9]+.[0-9]+.[0-9]+'` && \
#    wget https://github.com/mozilla/geckodriver/releases/download/$GECKODRIVER_VERSION/geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz &&\
#    tar -zxf geckodriver-$GECKODRIVER_VERSION-linux64.tar.gz -C /usr/local/bin && \
#    chmod +x /usr/local/bin/geckodriver

# install phantomjs
RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    tar -jxf phantomjs-2.1.1-linux-x86_64.tar.bz2 && cp phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin/phantomjs



COPY ./app /app
WORKDIR /app



# run server
EXPOSE 5001
CMD ["python", "main.py"]










#RUN apt-get install -y libgconf2-4 libnss3-1d libxss1
#RUN apt-get install -y fonts-liberation libappindicator1 xdg-utils

#RUN apt-get install -y software-properties-common





#
#
#RUN apt-get install -y python-software-properties
#RUN add-apt-repository -y ppa:ubuntu-mozilla-daily/ppa
#RUN apt-get update -y
#RUN apt-get install -y firefox
#
#
## install chromedriver and google-chrome
#RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
#    wget https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip
#
#RUN unzip chromedriver_linux64.zip -d /usr/bin
#RUN chmod +x /usr/bin/chromedriver
#
#
#RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
#RUN dpkg -i google-chrome*.deb
#RUN apt-get install -y -f


#RUN pip install selenium
#RUN pip install pyvirtualdisplay


#COPY ./app /app
#WORKDIR /app


# run server
#EXPOSE 5001
#CMD ["python", "main.py"]