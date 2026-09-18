# Python script to scrape an article given the url of the article and store the extracted text in a file
# Url: https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7

import os
import sys
import requests
import re
# Code here - Import BeautifulSoup library
from bs4 import BeautifulSoup
# Code ends here

try:
	import cloudscraper
	HAVE_CLOUDSCRAPER = True
except ImportError:
	HAVE_CLOUDSCRAPER = False

# function to get the html source text of the medium article
def get_page():
	global url
	
	# Code here - Ask the user to input "Enter url of a medium article: " and collect it in url
	url = input("Enter url of a medium article: ")
	# Code ends here
	
	# handling possible error
	if not re.match(r'https?://medium.com/',url):
		print('Please enter a valid website, or make sure it is a medium article')
		sys.exit(1)

	# Code here - Call get method in requests object, pass url and collect it in res
	headers = {
		'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'Accept-Language': 'en-US,en;q=0.9',
		'Accept-Encoding': 'gzip, deflate, br',
		'Connection': 'keep-alive',
		'Upgrade-Insecure-Requests': '1',
	}
	# Medium sits behind Cloudflare bot-protection that plain requests can trip a 403 on.
	# Use cloudscraper (a requests-compatible client built to solve Cloudflare's JS
	# challenge) when it's installed; otherwise fall back to a plain request.
	if HAVE_CLOUDSCRAPER:
		scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'darwin', 'mobile': False})
		res = scraper.get(url, headers=headers)
	else:
		res = requests.get(url, headers=headers)
	# Code ends here

	res.raise_for_status()
	soup = BeautifulSoup(res.text, 'html.parser')
	return soup

# function to remove all the html tags and replace some with specific strings
def clean(text):
    rep = {"<br>": "\n", "<br/>": "\n", "<li>":  "\n"}
    rep = dict((re.escape(k), v) for k, v in rep.items()) 
    pattern = re.compile("|".join(rep.keys()))
    text = pattern.sub(lambda m: rep[re.escape(m.group(0))], text)
    text = re.sub('\<(.*?)\>', '', text)
    return text


def collect_text(soup):
	text = f'url: {url}\n\n'
	para_text = soup.find_all('p')
	print(f"paragraphs text = \n {para_text}")
	for para in para_text:
		text += f"{para.text}\n\n"
	return text

# function to save file in the current directory
def save_file(text):
	if not os.path.exists('./scraped_articles'):
		os.mkdir('./scraped_articles')
	name = url.split("/")[-1]
	print(name)
	fname = f'scraped_articles/{name}.txt'
	
	# Code here - write a file using with (2 lines)
	with open(fname, 'w') as f:		
		f.write(text)

	# Code ends here

	print(f'File saved in directory {fname}')


if __name__ == '__main__':
	text = collect_text(get_page())
	save_file(text)
	# Instructions to Run this python code
	# Give url as https://medium.com/@subashgandyer/papa-what-is-a-neural-network-c5e5cc427c7