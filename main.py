import os
import time
import urllib
import configparser

from bs4 import  BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


# Define global variables (from config file)
config = configparser.ConfigParser()
config.read('config.ini')
glob_user = config['login']['username']
glob_pw = config['login']['password']
glob_link = config['anime']['link'] 
anime_name = config['anime']['name']
glob_folder = anime_name


# Prepare for files/folders for download
try:
	os.mkdir(glob_folder)
	print('Directory made')
except:
	pass
os.chdir(glob_folder)
print('Directory changed')

files = os.listdir()
if 'trackCopied.txt' in files:
	f = open('trackCopied.txt','r')
	m_in = f.read()
	m_in = int(m_in) + 1
	f.close()
else:
	m_in=0

if 'trackDownloaded.txt' in files:
	f = open('trackDownloaded.txt','r')
	j_init = f.read()
	j_init = int(j_init) + 1
	f.close()
else:
	j_init=0


# Run firefox with selenium
driver = webdriver.Firefox()
driver.set_page_load_timeout(100)


# Log into kissanime 
driver.get("https://kissanime.to/Login")
time.sleep(8)
username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")
username.send_keys(glob_user)
password.send_keys(glob_pw)
password.send_keys(Keys.RETURN)
time.sleep(6)
print('Logged In')


# Create list of episodes (links)
driver.get(glob_link)
currentpage = driver.page_source
soup = BeautifulSoup(currentpage, 'html.parser')
EpsList = []

alltr = soup.find_all('tr')
for tr in alltr:
	alltd = tr.find_all('td')
	for td in alltd:
		alla = td.find_all('a')
		for link in alla:
			linx = link.get('href')
			EpsList.append(linx)

EpsList = EpsList[::-1]
nEps = len(EpsList)
print('No of Episodes: '+str(nEps))
mainDom = 'https://kissanime.to'
epsLink=[]


# Create list of download links for each episode
for m in range(m_in,nEps):
	driver.get(mainDom+EpsList[m])
	time.sleep(5)
	page = driver.page_source
	soup = BeautifulSoup(page,'html.parser')
	divD = soup.find_all('div',{'id':'divDownload'})
	try:
		dLink = divD[0].a.get('href')
	except IndexError:
		time.sleep(5)
		page = driver.page_source
		soup = BeautifulSoup(page,'html.parser')
		divD = soup.find_all('div',{'id':'divDownload'})
		dLink = divD[0].a.get('href')
	epsLink.append(dLink)
	f = open('links.txt','a')
	f.write(dLink+'\n')
	f.close()

	f=open('trackCopied.txt','w')
	f.write(str(m))
	f.close()
	print('Copied Download Link for Episode '+str(m+1))

driver.quit() # Exit Selenium


# Download episodes
f = open('links.txt','r')
dLinks = f.readlines()

for j in range(j_init,nEps):	
	dLink = dLinks[j]
	ep_num = str(j+1)
	ep_num = ep_num.rjust(3,'0')
	f_name = anime_name+' - '+ep_num + '.mp4'
	print(f_name)
	urllib.request.urlretrieve(dLink,f_name)
	f=open('trackDownloaded.txt','w')
	f.write(str(j))
	f.close()


# End of script