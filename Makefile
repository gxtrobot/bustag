PYTHON3=python3

javbus:
	rm bus.db 
	$(PYTHON3) -m bustag.spider.bus_spider https://www.cdnbus.bid

pep8:
	pep8 *.py

wc:
	grep -v '^ *\(#.*\)\?$$' crawling.py | wc -l
