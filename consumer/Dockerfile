FROM python:3.7
MAINTAINER Peter Cornelius <peter@grabango.com>

# Dir setup
ENV APP_DIR /app
RUN mkdir ${APP_DIR}
VOLUME ${APP_DIR}
WORKDIR ${APP_DIR}

# Install requirements early so we can change code and re-build quickly
COPY ./consumer/requirements.txt .
RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# copy config files into filesystem
COPY ./consumer/src .
COPY ./event_reader/src .

# execute start up script
# I need a bash file to initialize the db (postgres?)
ENTRYPOINT ["python3", "app.py"]