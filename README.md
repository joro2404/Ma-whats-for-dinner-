# Ma-whats-for-dinner

![Logo](/app/static/img/core-img/logo.png)

Ma what's for dinner?  
In this web app you can check what you have in your fridge back home, what recipes you are able to cook with the products that you have and also discover new recipes.
You can create recipes, share them with friends and other users, rate the recipes etc.
The app tells you if you can cook a given ecipe with your current available products and many more!
The project is a combination of two school projects. The hardware part are sensors in the fridge that tell you what products you have.


## Demo and more
[Video Demo](https://youtu.be/TdikHEJOIYo)<br/>
[Hardware Repo](https://github.com/veselin-angelov/ma-whats-for-dinner-hardware)

## Installation instructions

1. Clone the repo
  ```
  $ git clone https://github.com/joro2404/Ma-whats-for-dinner-.git
  $ cd Ma-whats-for-dinner-
  ```

2. Initialize and activate a virtualenv:
  ```
  $ virtualenv -venv
  $ source venv/bin/activate
  ```

3. Install the dependencies:
  ```
  $ pip install -r requirements.txt
  ```

5. Run the development server:
  ```
  $ flask run
  ```

6. Navigate to [http://localhost:5000](http://localhost:5000)

## Technolgies

* [Flask](https://flask.palletsprojects.com/en/1.1.x/) - Flask is a micro web framework written in Python.
* [Jinja](https://jinja.palletsprojects.com/en/2.11.x/) - Jinja is a templating language for Python.
* [SQLite](https://www.sqlite.org/index.html) - SQLite is a SQL database engine.
* [HTML5](https://developer.mozilla.org/en-US/docs/Web/HTML) - HTML defines the meaning and structure of web content.
* [CSS3](https://developer.mozilla.org/en-US/docs/Archive/CSS3) - CSS is used to describe web page's appearance/presentation.
* [JavaScript](https://www.javascript.com/) - JavaScript is used for functionality/behavior of the web page.

## Authors

**Veselin Angelov** - *Programer, Hardware* - [veselin-angelov](https://github.com/veselin-angelov)<br/>
**Georgi Lyubenov** - *Programer, Hardware* - [joro2404](https://github.com/joro2404)

## Project Stats
[![Coverage Status](https://coveralls.io/repos/github/joro2404/Ma-whats-for-dinner-/badge.svg?branch=master)](https://coveralls.io/github/joro2404/Ma-whats-for-dinner-?branch=master)  

[![Build Status](https://travis-ci.org/joro2404/Ma-whats-for-dinner-.svg?branch=master)](https://travis-ci.org/joro2404/Ma-whats-for-dinner-)