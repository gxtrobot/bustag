PYTHON3=python3

javbus:
	$(PYTHON3) -m bustag.spider.bus_spider https://www.cdnbus.bid

recommend:
	$(PYTHON3) -m bustag.model.classifier

pep8:
	pep8 *.py

wc:
	grep -v '^ *\(#.*\)\?$$' crawling.py | wc -l
