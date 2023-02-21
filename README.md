# General description

In order to highlight my knowledge both in the development of web and data applications, I chose to develop a web service with a artificial intelligence that can predict Tesla shares on the stock market. The objective of this application is to predict the closing price of the day's stock, in terms of : its opening value (open), its highest value (high), its lowest value (low), and its volume (volume).

# Installation procedure

**info**: the project was developed under a Unix environment, so the installation procedure
only concerns OS such as Linux or Mac.
IDE: PyCharm.

Python version: **3.10.6 or 3.10.7**

**linux**
1) Installing Python:
* sudo apt-get update
* sudo apt-get install python3.10 or sudo apt-get install python3
* python3 --version
2) Installing poetry with curl:
* curl -sSL https://install.python-poetry.org | python3-
* poetry --version
3) Installing the project:
* poetry install
* poetry shell
* poetry env info
* poetry env use 3.10.7 (in case the correct version of python is not installed)
* poetry env list
4) To launch the API:
* poetry run app

**mac**
1) Python installation -> natively installed on Mac
2) Install poetry with homebrew: brew install poetry
3) Installing the project:
* poetry install
* poetry shell
* poetry env info
* poetry env use 3.10.7 (in case the correct version of python is not installed)
* poetry env list
4) To launch the API:
* poetry run app

**Under PyCharm, it would be necessary to add the correct interpreter .venv/bin/python3 otherwise the project
will not launch!**
