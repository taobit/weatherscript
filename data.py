#!/usr/bin/python
from urllib2 import urlopen
import datetime
import glob	# finds all pathnames matching a specified pattern
import re,os,json
# the place where store urls
url = 'http://copper.math.buffalo.edu/463/weatherpages/'



html = urlopen(url)



# Get the page content
source = html.read()



pagecomp = re.compile('<div class="defaultBlock"><a href="(.*)">')



results = re.findall(pagecomp, source)



def output(data, filename):
	try:
		jsondata = simplejson.dumps(data, indent=4, skipkeys=True, sort_keys=True)
		fd = open(filename, 'w')
		fd.write(jsondata)
		fd.close()
	except:
		print 'ERROR'
		pass



# Get the ten pages URL
tens = []
for page in results:
    if 'www.weather.com_weather_tenday_Buffalo_NY_14221' in page and '10-01' in page:
        tens.append(page)



tenhighcomp = re.compile('"wx-temp"> (.*)<sup>')
tenlowcomp = re.compile('"wx-temp-alt"> (.*)<sup>')
tendatecomp = re.compile('"wx-label">(.* .*)<')
count = 5



for ten in tens:
    filename = ten[5:10] + '.json'
    website = url + ten
    tenpage = urlopen(website)
    p = tenpage.read()
    tenhighs = re.findall(tenhighcomp, p)
    tenlows = re.findall(tenlowcomp, p)
    dates = re.findall(tendatecomp, p)
    tendates = []
    data = []
    ll = []
    for date in dates:
        if ('Observed High' in date) or ('12:25 pm' in date):
            continue
        tendates.append(date)
    #with open(filename, 'w') as outfile:
    for d, h, l in zip(tendates, tenhighs, tenlows):
        data = {'date': d, 'high': h, 'low': l}
        ll.append(json.dumps(data))
            #json.dump(ll, outfile, sort_keys = True, indent = 4, ensure_ascii=False)
    with open(filename, 'w') as outfile:
        outfile.write(json.dumps(ll, sort_keys = True, indent = 4, ensure_ascii=False))



