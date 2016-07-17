from bs4 import BeautifulSoup
from tabulate import tabulate
from fake_useragent import UserAgent
from urllib2 import Request, urlopen
import re
USER_AGENT = UserAgent()
TrackingNumbers = []

with open("ups.txt", 'r') as f_in:
	TrackingNumbers = filter(None, (line.rstrip() for line in f_in))

for trcknum in TrackingNumbers:
	print trcknum
	track_table = []
	req = Request("https://wwwapps.ups.com/WebTracking/track?track=yes&trackNums="+trcknum+"&loc=en_gb")
	req.add_header('User-Agent',USER_AGENT.random)
	page = urlopen(req).read()	
	soup = BeautifulSoup(page,'html.parser')
	rows = soup.find('table',{'class':'dataTable'}).findAll('tr')
	for row in rows:
		cols = [re.sub('\s+', ' ', ele.text.strip()).encode('ascii') for ele in row.findAll('td')]
		if cols: track_table.append([ele for ele in cols])

	print tabulate(track_table, headers =['Location','Date','Time','Info'],tablefmt="grid")

