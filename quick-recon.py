#!/usr/bin/env python
# quick-recon.py (v.0.1) - Do some quick reconnaissance on a domainbased web-application
# written by SI9INT (twitter.com/si9int) | si9int.sh

import urllib3, requests, json
import argparse
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser()
parser.add_argument('domain', help = 'domain (by URL;e.g. https://test.de)', type = str)

args = parser.parse_args()

whatcms_token = '756ab2cfa1ed5575a71e0714ef05c2e228f17b6b1476de7075f7f4d6b4978272376fb3'
domain = args.domain

def getOptions():
	http = urllib3.PoolManager()
	request = http.request('OPTIONS', domain, retries=False, redirect=False)

	try:
		allow = str(r.headers['Allow'])
		if allow:
			print('[-] Allowed HTTP-methods: ' + allow)
		else:
			print('[!] HTTP-OPTIONS failed')
	except:
		print('[!] HTTP-OPTIONS failed')
		pass

def getHeaders():
	headers = requests.get(domain).headers
	server = ''

	print('[-] HTTP-response header:\n---')
	for key,value in headers.items():
		print('\t' + key + ': ' + value)

		if key == 'Server':
			server = value

	if server:
		print('---\n[-] Webserver detected: ' + server)
	else:
		print('---\n[!] No "Server"-header')

def getCMS():
	request = requests.get('https://whatcms.org/APIEndpoint/Detect?url=' + domain + '&key=' + whatcms_token)
	response = json.loads(request.text)

	status = response['result']['code']

	if 'retry_in_seconds' in response:
		print('[-] CMS-API overload, try again i: ' + str(response['retry_in_seconds']) + 's')
	else:
		if status == 200:
			print('[-] CMS detected: ' + response['result']['name'])
		else:
			print('[!] No CMS detected')

def getTechnology():
	html = requests.get('http://w3techs.com/siteinfo.html?fx=y&url=' + domain).text
	soup = BeautifulSoup(html, 'lxml')
	table = soup.findAll('table', attrs={'class':'w3t_t'})[0]
	trs = table.findAll('tr')

	print('[-] W3-technologies:\n--')

	for tr in trs:
		th = tr.find('th')
		td = tr.find('td').text
		
		if td[-7:] == 'more...':
			td = td[:-9]
		
		print('\t' + th.text + ': ' + td)

	print('--')

def getRobots():
	request = requests.get(domain + '/robots.txt')
	
	if(request.status_code == 200):
		print('[-] Fetched robots.txt:\n--')
		lines = filter(None, request.text.split('\n'))
		
		for line in lines:
			print('\t' + line)
		
		print('--')
	else:
		print('[!] No robots.txt')

def getInteresting():

	# thanks to snallygaster (github.com/hannob)
	files = [
		'.idea/WebServers.xml', 'config/databases.yml', '.git/config', '.svn/entries', 'server-status', 'filezilla.xml', 'sitemanager.xml',
		'.DS_Store', '_FILE_.bak', 'dump.sql', 'database.sql', 'backup.sql',
		'data.sql', 'db_backup.sql', 'db.sql', 'localhost.sql', 'mysql.sql', 'site.sql',
		'temp.sql', 'users.sql', 'app/etc/local.xml', 'server.key', 'key.pem', 'id_rsa', 'id_dsa',
		'.env', '.ssh/id_rsa', '.ssh/id_dsa', 'cgi-bin/cgiecho', 'cgi-sys/cgiecho', 'winscp.ini', 'sites/default/private/files/backup_migrate/scheduled/test.txt', 
	]

	print('[!] Checking interesting files')

	for count, file in enumerate(files):
		req = requests.get(domain + '/' + file)

		if count == 16:
			print('[-] Checked 50% of dictionary')
		if req.status_code == 200:
			print('[-] Found interesting file: /' + file)

recon = [
	getOptions,
	getHeaders,
	getTechnology,
	getCMS,
	getRobots,
	getInteresting
]

for module in recon:
	module()

print('[!] Finished quick-reconnaissance on: ' + domain)