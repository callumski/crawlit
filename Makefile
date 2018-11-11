VIRTUALENV=env
V_PATH=$(VIRTUALENV)/bin
V_COMMAND=source $(V_PATH)/activate;
TIME_NOW=$(shell date -u '+%s')

.PHONY: all run

all: clean setup test run crawl display

clean:
	rm -f crawlit/*.pyc
	rm -rf $(VIRTUALENV)
	rm -rf output

setup:
	python3 -m venv $(VIRTUALENV)
	$(V_COMMAND) pip install --upgrade setuptools
	$(V_COMMAND) pip install -r requirements.txt
	$(V_COMMAND) pip install -e .
	mkdir output

test:
	$(V_COMMAND) python3 -m pytest --verbose

run:
	CRAWLIT_JSON_FILE=output/crawlit.${TIME_NOW}.json	${MAKE} crawl  ${MAKE} display


crawl:
	${CRAWLIT_JSON_FILE:=output.json} ;	$(V_COMMAND) scrapy crawl -a url=${url} spider -o ${CRAWLIT_JSON_FILE} -t jsonlines

display:
	$(V_COMMAND) python3 crawlit/display.py ${CRAWLIT_JSON_FILE} -ob
