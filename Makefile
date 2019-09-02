PYTHON3=python3

javbus:
	$(PYTHON3) -m bustag.main download

recommend:
	$(PYTHON3) -m bustag.main recommend

build:
	docker build -t  bustag-app-dev .
	
run:
	docker run --rm -d -v `pwd`/data:/app/data -p 8080:8080 bustag-app-dev 

server:
	$(PYTHON3) bustag/app/index.py

publish:
	docker tag bustag-app-dev gxtrobot/bustag-app:latest
	docker push gxtrobot/bustag-app:latest