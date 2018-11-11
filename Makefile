VIRTUALENV=env
V_PATH=$(VIRTUALENV)/bin
V_COMMAND=source $(V_PATH)/activate;
TIME_NOW=$(shell date -u '+%d.%m.%y-%H.%M.%s')

setup:
	python3 -m venv $(VIRTUALENV)
	$(V_COMMAND) pip install --upgrade setuptools
	$(V_COMMAND) pip install -r requirements.txt
	$(V_COMMAND) pip install -e .
	mkdir output

clean:
	rm -f crawlit/*.pyc
	rm -rf $(VIRTUALENV)

test:
	$(V_COMMAND) python3 -m pytest --verbose

run: crawl display

crawl:
	$(V_COMMAND) scrapy crawl -a url=${url} spider -o output/crawlit.${TIME_NOW}.json -t jsonlines

display:
	$(V_COMMAND) python3 crawlit/display.py
