FROM python:3.7.4-slim as base

# Create app directory
WORKDIR /app

# Install app dependencies
COPY ./docker/sources.list .

RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && mv ./sources.list /etc/apt/

RUN apt-get -o Acquire::Check-Valid-Until=false update \
    && apt-get install \
    --no-install-recommends --yes \
    build-essential libpq-dev cron \
    python3-dev --yes

FROM base as build

COPY requirements.txt .

RUN mkdir /install

RUN pip download --destination-directory /install -r /app/requirements.txt -i https://pypi.douban.com/simple

FROM python:3.7.4-slim  as release

COPY ./docker/sources.list .

RUN mv /etc/apt/sources.list /etc/apt/sources.list.bak && mv ./sources.list /etc/apt/

RUN apt-get update && apt-get -y install cron

WORKDIR /app

COPY ./docker/crontab.txt /etc/cron.d/crontab.txt

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/crontab.txt

RUN crontab /etc/cron.d/crontab.txt

COPY --from=build /install /install

COPY requirements.txt .

RUN pip install --no-index --find-links=/install -r requirements.txt

COPY . /app

RUN pip install -e .

RUN touch /var/log/bustag.log

RUN rm -rf /install &&  rm -rf /root/.cache/pip

RUN chmod 755 /app/docker/*.sh

EXPOSE 8080

CMD ["/app/docker/entry.sh"]