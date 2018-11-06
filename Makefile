VIRTUALENV=env
V_PATH=$(VIRTUALENV)/bin
V_COMMAND=source $(V_PATH)/activate;

setup:
	python3 -m venv $(VIRTUALENV)
	$(V_COMMAND) pip install --upgrade setuptools
	$(V_COMMAND) pip install -r requirements.txt
	$(V_COMMAND) pip install -e .

clean:
	rm -f crawlit/*.pyc
	rm -rf $(VIRTUALENV)

test:
	$(V_COMMAND) python3 -m pytest -v

run:
	$(V_COMMAND) scrapy crawl -a url=${url} spider
