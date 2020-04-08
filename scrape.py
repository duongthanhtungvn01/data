import requests
import json
from bs4 import BeautifulSoup

url = "https://www.tradingview.com/ideas/waveanalysis/page-2/"
text = requests.get(url).text
doc = BeautifulSoup(text)
divs = doc.findAll("div", {"class": "tv-feed-layout__card-item"})

items = []
for div in divs:
	data = json.loads(div['data-widget-data'])
	data2 = json.loads(div['data-card'])
	div2 = div.find("div", {"class" :"tv-widget-idea__social-row"})
	data3 = json.loads(div2["data-model"])
	span = div.find("span", {"class":"tv-card-stats__time js-time-upd"})
	span2 = div.find("span", {"class":"tv-widget-idea__timeframe"})
	span3 = div.find("span", {"class":"tv-widget-idea__label"})
	p = div.find("p", {"class": "tv-widget-idea__description-row"})
	up = True if span3 and "tv-idea-label--long" in span3["class"] else False
	down = True if span3 and "tv-idea-label--short" in span3["class"] else False
	items.append( {
		"id": data["id"],
		"title": data["name"],
		"description": p.text.strip(),
		"published_chart_url": "https://www.tradingview.com" + data["published_chart_url"],
		"author": data2["author"]["username"],		
		"item": {
			"symbol": data["short_symbol"],
			"timeframe": span2.text.replace(',','').strip(),
			"direction": "up" if up else ("down" if down else "")
		},
		"likescore": data["like_score"],
		"commentsCount": data3["commentsCount"],
		"publishedTimestamp" : span["data-timestamp"]
		
	})
	
print(json.dumps(items, indent=4))
