FROM python:3.7
MAINTAINER Peter Cornelius <peter@grabango.com>

# Install base components
# RUN apk add --no-cache python3

# Dir setup
ENV APP_DIR /app
RUN mkdir ${APP_DIR}
VOLUME ${APP_DIR}
WORKDIR ${APP_DIR}

# when modifying requirements be sure to rebuild the individual service (buggy docker-compose crap)!!
COPY ./api_producer/requirements.txt .

RUN pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# expose http port
# EXPOSE 80

# copy files into filesystem
COPY ./api_producer/src .
COPY ./event_publisher/src .

# execute start up script
ENTRYPOINT ["python3", "app.py"]