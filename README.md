## kissanime-download
Downloads animes from the website [kissanime](http://kissanime.to). If by any chance the script is interrupted before it completes downloading all episodes, running it again will continue from where it left off.
If you are using a unix system, you can use threaded-download which will downloaded multiple files at the same time, ensuring faster download.

### Dependencies
1. [Python 3](https://www.python.org/)
2. [Selenium](https://pypi.python.org/pypi/selenium) python package. Install as `pip3 install selenium`
3. [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/) python package. Install as `pip3 install beautifulsoup4'
4. [pySmartDL](https://pypi.python.org/pypi/pySmartDL/) .Install as `pip3 install pySmartDL`
5. Firefox Webbrowser

### How to run
1. Add username and password in config.ini
2. Add anime url and name
3. Run as `python3 download.py`
4. For unix users who want faster download, run as `python3 threaded-download.py`