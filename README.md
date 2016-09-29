## kissanime-download
Downloads animes from the website [kissanime](http://kissanime.to). If by any chance the script is interrupted before it completes downloading all episodes, running it again will continue from where it left off.
Download.py downloads one file at a time.
Threaded-download will downloaded multiple files at the same time, ensuring faster download.

### Dependencies
1. [Python 3](https://www.python.org/)
2. [Selenium](https://pypi.python.org/pypi/selenium) python package. Install as `pip3 install selenium`
3. [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/) python package. Install as `pip3 install beautifulsoup4`
4. [pySmartDL](https://pypi.python.org/pypi/pySmartDL/) .Install as `pip3 install pySmartDL`
5. Firefox Webbrowser

### How to run
1. Add username and password in config.ini
2. Add anime url and name
3. Run as `python3 download.py`
4. For users who want faster download, run as `python3 threaded-download.py`

### !Replacement for Selenium
A better solution would be to silently open the browser (in the background) and hit the URLs and parse the source code etc. Possible solutions might be foundhere:
1. http://stackoverflow.com/questions/16180428/can-selenium-webdriver-open-browser-windows-silently-in-background
2. https://www.quora.com/What-are-some-great-alternatives-to-selenium-testing
3. http://stackoverflow.com/questions/5370762/how-to-hide-firefox-window-selenium-webdriver
4. http://stackoverflow.com/questions/1418082/is-it-possible-to-hide-the-browser-in-selenium-rc
