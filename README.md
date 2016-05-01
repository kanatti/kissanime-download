## kissanime-download
Downloads anime from the website [kissanime](http://kissanime.to). If the download of an episode is interrupted, it skips that episode and downloads rest of the series. In the end, it will show list of failed downloads. If again, by any chance the script is interrupted before it completes downloading all episodes, running it again will continue from where it left off.

### Dependencies
1. [Python 3](https://www.python.org/)
2. [Selenium](https://pypi.python.org/pypi/selenium) python package. Install as `pip3 install selenium`
3. [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/) python package. Install as `pip3 install beautifulsoup4'
4. [Simpleaudio](http://simpleaudio.readthedocs.io/en/latest/index.html) python package. Install as `pip3 install simpleaudio`
5. Firefox Webbrowser

### How to run
0. Use short-downloader.py for downloading series with less than 30 episodes. Use long-downloader.py for longer series.
1. Add username and password in  long-config.ini or short-config.ini file.
2. Add anime url and name
3. Run as `python3 long-downloader.py` or `python3 short-downloader.py`