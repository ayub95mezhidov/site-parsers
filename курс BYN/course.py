import os
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup



def get_course():

	print("please wait...")
	
	url = "https://select.by/kurs/"

	headers = {
		"user-agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36",
		"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"
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
	card = soup.find("div", class_="pt-2").find_all("tr", class_="text-center h4")
	for item in card:
		count = item.find_all("td")[0].text
		currency = item.find_all("td")[1].text
		today = item.find_all("td")[2].text.strip()
		tomorrow = item.find_all("td")[3].find_all("span")[1].text.strip()
		#print(f"{count} {currency}        на сегодня BYN {today},        на завтра BYN {tomorrow}")

		data.append({
			"currency" : f"{count} {currency}",
			"today" : f"BYN {today}",
			"tomorrow" : f"BYN {tomorrow}",
			})


	cur_date = datetime.now().strftime("%d_%m_%Y")
	with open(f"data/course_BYN_{cur_date}.json", "w") as file:
		json.dump(data, file, indent=4, ensure_ascii=False)


def main():
	get_course()

if __name__ == '__main__':
	main()