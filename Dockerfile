FROM python:3.7.4-slim as base

# Create app directory
WORKDIR /app

# Install app dependencies
COPY requirements.txt .

COPY ./docker/sources.list .

RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && mv ./sources.list /etc/apt/

RUN apt-get -o Acquire::Check-Valid-Until=false update \
    && apt-get install \
    --no-install-recommends --yes \
    build-essential libpq-dev \
    python3-dev --yes

from base as build

RUN mkdir /install

RUN pip download --destination-directory /install -r /app/requirements.txt -i https://pypi.douban.com/simple

from python:3.7.4-slim  as release

WORKDIR /app

COPY --from=build /install /install

COPY . /app

RUN pip install --no-index --find-links=/install -r requirements.txt

RUN pip install -e .

RUN rm -rf /install &&  rm -rf /root/.cache/pip


EXPOSE 8080

CMD [ "python", "bustag/app/index.py" ]