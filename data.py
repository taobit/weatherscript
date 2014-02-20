import re,os,datetime,json
from urllib2 import urlopen

response = urlopen('http://www.weather.com/weather/tenday/Buffalo+NY+USNY0181:1:US')
real = urlopen('http://www.weather.com/weather/yesterday/Buffalo+NY+14221:4:US')
html = response.read()
rhtml = real.read()
highcomp = re.compile('"wx-temp"> (.*)<sup>')
lowcomp = re.compile('"wx-temp-alt"> (.*)<sup>')
datecomp = re.compile('"wx-label">(.* .*)<')
yestcomp = re.compile('"wx-temp">(.*)<span>')
highs = re.findall(highcomp, html)
lows = re.findall(lowcomp, html)
dates = re.findall(datecomp, html)
yesterday = re.findall(yestcomp, rhtml)
now = datetime.date.today()
weatherfile = 'myweatherfile_' + str(now) + '.json'
os.chdir('weather')
with open(weatherfile, 'w') as outfile:
	for d, h, l in zip(dates, highs, lows):
		data = {'date': d, 'high': h, 'low': l}
		json.dump(data, outfile, indent = 4)
yest = dates[0].split(" ")
with open(weatherfile, 'a+b') as outfile:
	y = yest[0] + " " + str(int(yest[-1]) - 1)
	data = {'yesterday': y, "high": yesterday[0], "low": yesterday[1]}
	json.dump(data, outfile, indent = 4)