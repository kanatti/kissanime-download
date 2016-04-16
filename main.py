import time
import configparser
import os
import urllib
from bs4 import  BeautifulSoup
from selenium import webdriver
# from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys

# =========== DEFINE GLOBAL VERIABLES ===========
config = configparser.ConfigParser()
config.read('config.ini')
glob_user = config['login']['username']
glob_pw = config['login']['password']
glob_link = config['anime']['link'] 
anime_name = config['anime']['name']
glob_folder = anime_name
#glob_cont = 0

try:
	os.mkdir(glob_folder)
	print('Directory made')
except:
	pass
os.chdir(glob_folder)
print('Directory changed')

files = os.listdir()
if 'n.txt' in files:
	f = open('n.txt','r')
	m_in = f.read()
	m_in = int(m_in) + 1
	f.close()
else:
	m_in=0

if 'j.txt' in files:
	f = open('j.txt','r')
	j_init = f.read()
	j_init = int(j_init) + 1
	f.close()
else:
	j_init=0
# =========== DEFINE GLOBAL VERIABLES ===========



driver = webdriver.Firefox()
driver.set_page_load_timeout(100)
driver.get("https://kissanime.to/Login")
time.sleep(8)

# locate username and password fields in the login page
username = driver.find_element_by_id("username")
password = driver.find_element_by_id("password")

# type login info into fields
username.send_keys(glob_user)
password.send_keys(glob_pw)

# send the filled out login form and wait
password.send_keys(Keys.RETURN)
time.sleep(6)
print('Logged In')


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
print('No of eps '+str(nEps))
mainDom = 'https://kissanime.to'
epsLink=[]

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

	f=open('n.txt','w')
	f.write(str(m))
	f.close()
	print('HTML ep num: '+str(m+1))


driver.quit()

# SELENIUM ENDS ====================================


f = open('links.txt','r')
dLinks = f.readlines()	

for j in range(j_init,nEps):	
	dLink = dLinks[j]
	f_name = anime_name+' - '+str(j+1)
	print(f_name)
	urllib.request.urlretrieve(dLink,f_name)
	f=open('j.txt','w')
	f.write(str(j))
	f.close()