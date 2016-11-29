FROM python:3.5
ENV PYTHONUNBUFFERED 1

# User defined.  See docker-compose.yml at web.build.args
ARG env

RUN curl -sL https://deb.nodesource.com/setup_6.x | bash
RUN apt-get update;
RUN apt-get install nodejs ruby -y;
RUN gem install sass;
RUN npm install -g bower

WORKDIR /app
ADD requirements/*.txt /app/requirements/
RUN bower install --allow-root
RUN pip install -r requirements/$env.txt
ADD . /app
