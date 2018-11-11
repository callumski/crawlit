# crawlit
A simple web crawler built using [Scrapy](https://scrapy.org/).



## Overview

**crawlit** is limited to one domain. Given a starting URL – say http://www.example.com - it will visit all pages within the domain, but not follow the links to external sites such as Google or Twitter.

**crawlit** works in 2 stages:

1. crawl
	* **crawlit** crawls the given domain finding all internal an external links and static content, recording what it finds in a JSON Lines file
2. display
	* **crawlit** parses the JSON Lines file and renders it into a HTML file which can be viewed in the web browser of your choice

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

N.B. Running  ```make all``` also runs ```make clean``` which will remove the virtualenv, any Python bytecode files and the ```./output``` folder.

## Running the tests
The tests are written using [pytest](https://pytest.org). To run them:

```
$ make test
```
N.B. **crawlit** has been tested with Python 3 on OSX High Sierra.

## Usage
To crawl the domain [www.example.com](http://www.example.com), have it rendered and then displayed in your default web browser:

```
$ make run url=http://www.example.com
```
N.B. The whole URL including scheme is necessary.



To crawl the domain [www.example.com](http://www.example.com):

```
$ make crawl url=http://www.example.com
```
N.B. The whole URL including scheme is necessary.

This will write a [JSON Lines](http://jsonlines.org/) file to the ```./output``` folder. The file will be name ```crawlit.NNNNNNNNNN.json```. Where NNNNNNNNNN is the system time since Epoch in milliseconds.

To render and display a given **crawlit** JSON file:

```
$ CRAWLIT_JSON_FILE=path.to/crawlit.NNNNNNNNNN.json make display
```

## Approach taken
As it offers a fully featured framework for web-scraping [Scrapy](https://scrapy.org/) was chosen. This prevented having to reinvent the wheel and gave several important features out of the box (including auto-throttling, respecting ```robots.txt```, parallel downloads, xpath navigation, a variety of output formats).

[JSON Lines](http://jsonlines.org/) was chosen as an output format as it will generate a valid JSON file, even if the crawler is stopped before completing the crawl of the website. It also means that the output can be parsed in a memory efficient way if necessary.

Each page is represented as a single CrawlitItem object. This allows for simple atomic processing of each page, the list of internal links for each page would allow a graph of the pages to be easily generated from the list of items.

The displaying of the output by rendering it to an HTML file with Jinja2 was chosen due to the simplicity of implementation. For a very large site the HTML file might grow too large, pagination could help with this, also the rendering could be avoided if output JSON was loaded using javascript. This was beyond scope of this project. The styling of the HTML is pretty barebones, again chosen due to ease of implementation.


## Possible extensions:

The following extensions are possible:

* Better handling of non-HTTP schemes. ```mailto:``` and ```tel:``` are not treated specifically
* Tests for the HTML rendering
* Error checking for the absence of schema on input domain
* Add the ability to recommence a crawl that was stopped. This could be done by passing in the output from a previous crawl to populate the list of parsed pages
* In the HTML display, we could allow navigation between internal pages in sitemap. Currently the links are to the actual URL's but it might be nicer to be able to navigate the sitemap
* Validation of functionality on other operating systems
* Better data handling for very large websites. It is possible the current display functionality would be too resource intensive for very large domains
* Giving it an end-to-end HTML UI to allow it to be deployed as a web application
* Storing of output in a database
