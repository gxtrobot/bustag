PYTHON3=python3

javbus:
	$(PYTHON3) -m bustag.spider.bus_spider https://www.cdnbus.bid

recommend:
	$(PYTHON3) -m bustag.main recommend

build:
	docker build -t  bustag-app-dev .
	
run:
	docker run --rm -d -v `pwd`/data:/app/data -p 8080:8080 bustag-app-dev 

server:
	gunicorn bustag.app.index:app --bind='0.0.0.0:8080'

publish:
	docker tag bustag-app-dev gxtrobot/bustag-app:latest
	docker push gxtrobot/bustag-app:latest