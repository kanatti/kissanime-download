import os
import math
import time
import urllib
import configparser
import multiprocessing

from bs4 import  BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import simpleaudio

#Function called  in each thread 
def download(args):
	url = args[0]
	start = args[1]
	end = args[2]
	part = args[3]

	req = urllib.request.Request(url)
	req.headers['Range'] = 'bytes=%s-%s' % (start, end)
	f = urllib.request.urlopen(req)

	chunk_size = 16 * 1024
	with open("temp"+str(part)+".mp4", "ab") as temp_file:
		while True:
			chunk = f.read(chunk_size)
			if not chunk: break
			temp_file.write(chunk)


if __name__ == "__main__":
	#Define global variables (from config file)
	config = configparser.ConfigParser()
	config.read('small-config.ini')
	glob_user = config['login']['username']
	glob_pw = config['login']['password']
	glob_link = config['anime']['link'] 
	anime_name = config['anime']['name']
	glob_folder = anime_name

	parent_folder=os.getcwd() #Used for storing location of audio file

	info = configparser.ConfigParser()
	info['track'] = {'eps_num':'0', 'last_copy':'0', 'time_stamp':'0', 'last_download':'0'}


	#Prepare for files/folders for download
	try:
		os.mkdir(glob_folder)
		print('Directory made')
	except:
		print('Directory already exists')
	os.chdir(glob_folder)
	print('Directory changed')

	files = os.listdir()
	if 'info.ini' in files:
		info.read('info.ini')
		cur_time = time.time()
		delay = cur_time - float(info['track']['time_stamp'])
		ld = int(info['track']['last_download'])
		if delay<5400:
			lc = int(info['track']['last_copy'])
		else:
			print('Download Links Expired')
			lc = int(info['track']['last_download'])
			f = open("Links.txt", "w")
			for i in range(0,ld):
				f.write('Dummy Link\n')
			f.close()
	else:
		lc = 0
		ld = 0


	#Run firefox with selenium
	driver = webdriver.Firefox()
	driver.set_page_load_timeout(100)


	#Log into kissanime 
	driver.get("https://kissanime.to/Login")
	time.sleep(8)
	username = driver.find_element_by_id("username")
	password = driver.find_element_by_id("password")
	username.send_keys(glob_user)
	password.send_keys(glob_pw)
	password.send_keys(Keys.RETURN)
	time.sleep(5)
	print('Logged In')


	#Create list of episodes (links & names)
	if info['track']['eps_num']=='0':
		driver.get(glob_link)
		currentpage = driver.page_source
		soup = BeautifulSoup(currentpage, 'html.parser')
		EpsList = []
		NamesList=[]

		alltr = soup.find_all('tr')
		for tr in alltr:
			alltd = tr.find_all('td')
			for td in alltd:
				alla = td.find_all('a')
				for link in alla:
					linx = link.get('href')
					namex = link.contents[0].strip()+'.mp4'
					namex = namex.replace(':',' -')
					temp = linx.split('/')
					if temp[-1][0:7] == 'Episode':
						EpsList.append(linx)
						NamesList.append(namex)
						
		nEps = len(EpsList)
		info['track']['eps_num'] = str(nEps)
		with open('info.ini', 'w') as info_file:
			info.write(info_file)
		EpsList = EpsList[::-1]
		NamesList = NamesList[::-1]
		for ind in range(0,nEps):
			with open("EpisodeLinks.txt", "a") as elnks:
				elnks.write(EpsList[ind]+'\n')
			with open("EpisodeNames.txt", "a") as enms:
				enms.write(NamesList[ind]+'\n')
		print('No of Episodes: '+str(nEps))


	#Read episode data from text files
	f0 = open("EpisodeLinks.txt","r")
	EpsList = f0.read()
	f0.close()
	EpsList = EpsList.split('\n')[0:-1]
	f0 = open("Episodenames.txt","r")
	NamesList = f0.read()
	f0.close()
	NamesList = NamesList.split('\n')[0:-1]

	nEps = int(info['track']['eps_num'])
	mainDom = 'https://kissanime.to'


	#Create list of download links for each episode
	print('Copied download link for episodes:')
	
	for m in range(lc,nEps):
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
		
		with open("Links.txt", "a") as lnks:
			lnks.write(dLink+'\n')
		info['track']['last_copy'] = str(m+1)
		info['track']['time_stamp'] = str(time.time())
		with open('info.ini', 'w') as info_file:
			info.write(info_file)
		print(str(m+1))


	#Exit selenium
	driver.quit()


	#Download episodes using multithread urllib
	f = open('Links.txt','r')
	dLinks = f.read()
	f.close()
	dLinks = dLinks.split('\n')[0:-1]

	print("Download Started")
	failed_eps=[] #List of eps that couldn't be downloaded

	for j in range(ld,nEps):

		try:
			t_start = time.time()
			file_name = NamesList[j]
			dl_link = dLinks[j-ld]
			site = urllib.request.urlopen(dl_link)
			file_size = site.headers["Content-Length"]
			size_bytes = int(file_size)
			four_part = math.ceil(size_bytes/5)
			last_part = size_bytes - 4*four_part

			links = [dl_link]*5
			parts = list(range(1,6))
			starts=[]
			ends=[]
			for k in range(0,5):
				starts.append(k*four_part)
				ends.append((k+1)*four_part - 1)
			ends[4] = size_bytes-1
			args=list(zip(links,starts,ends,parts))
			args_list =[list(arg) for arg in args]
			pool=multiprocessing.Pool(processes=5)
			pool.map(download,args_list)

			for m in range(0,5):
				part_file = open("temp"+str(m+1)+".mp4", "rb")
				data = part_file.read()
				part_file.close()
				with open(file_name, "ab") as code:
					code.write(data)
				os.remove("temp"+str(m+1)+".mp4")

			info['track']['last_download'] = str(j+1)
			with open('info.ini', 'w') as info_file:
				info.write(info_file)

			t_end = time.time()
			dl_speed = size_bytes/(1024*1024*(t_end-t_start))
			print("Downloaded: "+file_name+" at %.2f MBPS" % dl_speed)
		
		except:
			file_name = NamesList[j]
			failed_eps.append(file_name)
			print("Download of "+file_name+" has FAILED")
			for m in range(0,5):
				try:
					os.remove("temp"+str(m+1)+".mp4")
				except:
					pass


	#Play audio on completion of download
	aud_file = os.path.join(parent_folder,'alarm.wav')
	audio_cue = simpleaudio.WaveObject.from_wave_file(aud_file)
	play_cue = audio_cue.play()
	play_cue.wait_done()

	print('Download Completed')
	if len(failed_eps)!=0:
		print('Failed Episodes:')
		for failed in failed_eps:
			print(failed)


# End of script	