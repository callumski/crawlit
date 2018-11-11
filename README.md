# crawlit
A simple web crawler built using [Scrapy](https://scrapy.org/).



## Overview

**crawlit** is limited to one domain. Given a starting URL – say http://www.example.com - it will visit all pages within the domain, but not follow the links to external sites such as Google or Twitter.

**crawlit** works in 2 stages:

1. crawl
	* **crawlit** crawls the given domain finding all internal an external links and static content, recording what it finds in a json-lines file
2. display
	* **crawlit** parses the json-lines file and renders it into a HTML file which can be viewed in the web browser of your choice

## Requirements
**crawlit** requires you have [Python3](https://www.python.org/downloads/) and [pip](https://pypi.org/project/pip/) installed.

Other required packages are downloaded during installation.

## Installation
To install **crawlit**:

```
$ git clone https://github.com/callumski/crawlit.git
$ cd crawlit
$ make setup
```
This will:

* download the git repository
* cd into the folder
* run a ```make``` command that creates a virtualenv and installs are the required dependencies

For convenience there is also:

```
$ make all
```
Which will setup **crawlit** and run the tests.

N.B. Running  ```make all``` also runs ```make clean``` which will remove the virtualenv, any python bytecode files and the ```./output``` folder.

## Running the tests
The tests are written using [pytest](https://pytest.org). To run them:

```
$ make test
```
N.B. **crawlit** has been tested with Python 3 on OSX High Sierra.

## Usage
To crawl the domain [www.example.com](http://www.example.com), have it rendered and then dsiplayed in your default web browser:

```
$ make run url=http://www.example.com
```
N.B. The whole URL including scheme is necesary.



To crawl the domain [www.example.com](http://www.example.com):

```
$ make crawl url=http://www.example.com
```
N.B. The whole URL including scheme is necesary.

This will write a [JSON Lines](http://jsonlines.org/) file to the ```./output``` folder. The file will be name ```crawlit.NNNNNNNNNN.json```. Where NNNNNNNNNN is the system time since Epoch in milliseconds.

To render and display a given **crawlit** json file:

```
$ CRAWLIT_JSON_FILE=path.to/crawlit.NNNNNNNNNN.json make display
```

## Approach taken
As it offers a fully featured framework for web-scraping [Scrapy](https://scrapy.org/) was chosen. This prevented having to reinvent the wheel and gave several important features out of the box (including auto-throttling, respecting ```robots.txt```, parallel downloads, xpath navigation, a variety of output formats).

[JSON Lines](http://jsonlines.org/) was chosen as an output format as it will generate a valid JSON file, even if the crawler is stopped before completing the crawl of the website. It also means that the output can be parsed in a memory efficient way if necessary.

Each page is represented as a single CrawlitItem object. This allows for simple atomic processing of each page, the list of internal links for each page would allow a graph of the pages to be easily generated from the list of items.

The displaying of the output by rendering it to an HTML file with Jinja2 was chosen due to the simplicity of implemtation. For a very large site the HTML file might grow too large, pagination could help with this, also the rendering could be avoided if output JSON was loaded using javascript. This was beyind scope of this project. The styling of the HTML is pretty barebones, again chosen due to ease of implentation.


## Further possible extensions:

The following extensions are possible:

* more tests for display html rendering
* better handling of non-html schemes
* error checking for absence of schema on input domain
* Add ability to recommence crawl that was stopped
* Allow navigation between internal pages in displayed sitemap
