FROM python:3.7.4-slim

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt /app
COPY ./docker/sources.list /app

RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && mv ./sources.list /etc/apt/

RUN apt-get -o Acquire::Check-Valid-Until=false update \
    && apt-get install \
    --no-install-recommends --yes \
    build-essential libpq-dev \
    python3-dev --yes

RUN pip install -r requirements.txt -i https://pypi.douban.com/simple

COPY . /app
RUN pip install -e .

EXPOSE 8080
CMD [ "python", "bustag/app/index.py" ]