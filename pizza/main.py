import os
import requests
import json
from bs4 import BeautifulSoup

def get_data():

	url = "https://www.pizzatempo.by/menu/pizza.html"
	
	headers = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
		"accept" : "*/*"
	}

	r = requests.get(url=url, headers=headers)

	if not os.path.exists('data'):
		os.mkdir("data")

	#with open("data/index.html", "w", encoding="utf-8") as file:
		#file.write(r.text)

	with open("data/index.html", "r", encoding="utf-8") as file:
		src = file.read()

	data = []
	soup = BeautifulSoup(src, 'lxml')
	previews = soup.find_all("div", class_="previews")
	for preview in previews:
		cards = preview.find_all("div", class_="info")
		for card in cards:
			title = card.find("div", class_="photo").find("img").get('alt')
			img_link = card.find("div", class_="photo").find("img").get('src')
			structure = card.find("div", class_="composition_holder").find("div", class_="composition").text.strip()
			print(title)

			data.append({
				"title" : title.replace('"', ' ').strip(),
				"img_link" : img_link,
				"structure" : structure
				})

	with open("data/data.json", "w", encoding="utf-8") as file:
		json.dump(data, file, indent=4, ensure_ascii=False)


def main():
	get_data()

if __name__ == '__main__':
	main()