import csv
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

def get_all_pages(url):
	headers = {
		"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
	}

	req = requests.get(url=url, headers=headers)
	#print(req.text)

	# Сохраняем страгицу
	with open("nfr_1.html", "w", encoding="utf-8") as file:
		file.write(req.text)

	# Открываем для чтения
	with open("nfr_1.html", "r", encoding="utf-8") as file:
		src = file.read()

	soup = BeautifulSoup(src, 'lxml')

	# Сохроняем все страницы
	pages_count = int(soup.find("div", class_="sc-4r7b5t-3 bvcQcm").find_all("a")[-2].text)
	for i in range(1, pages_count + 1):
		url = f"https://coinmarketcap.com/nft/upcoming/?page={i}"

		req = requests.get(url=url, headers=headers)

		with open(f"data4/nft_{i}.html", "w", encoding="utf-8") as file:
			file.write(req.text)


def get_data(pages_count):
	cur_date = datetime.now().strftime("%d_%m_%Y")

	# Создаем csv файл
	with open(f"data4/data_{cur_date}.csv", "w", encoding="utf-8") as file:
		writer = csv.writer(file)

		writer.writerow(
			(
				"Project",
				"Currency"
				"Links",
				"Starts in",
				"Sale info"
				)
			)

	data = []
	# Парсим данные с сайтов
	for page in range(1, 10):
		with open(f"data4/nft_{page}.html", "r", encoding="utf-8") as file:
			src = file.read()

		soup = BeautifulSoup(src, 'lxml')

		table = soup.find("div", class_="table").find("tbody")
		all_tr = table.find_all("tr")
		for tr in all_tr:
		
			div = tr.find("div", class_="sc-15yqupo-0 cqAZPF")
			name = div.find("p").find("span").text
			currency = div.find("p").find_all("span")[-2].text
			
			div_2 = tr.find("div", class_="sc-15yqupo-1 gEtvIk")
			website = div_2.find_all("a")[-1].get("href")
			twitter = div_2.find_all("a")[-2].get("href")
			discord = div_2.find_all("a")[-3].get("href")
			
			div_3 = tr.find("div", class_="sc-15yqupo-2 dhMNvT")
			starts_in_hours_ago = div_3.find_all("p")[0].text
			starts_in_date = div_3.find_all("p")[1].text

			div_4 = tr.find("div", class_="sc-1ay2tc4-0 dRIGnz")
			sale_info = div_4.find("span").text

			data.append(
				{
					"Project" : name,
					"Currency" : currency,
					"Links" : {
								"Discord" : discord, 
							   	"Twitter" : twitter, 
							   	"Website" : website
							   },
					"Starts in" : starts_in_date,
					"Sale info" : sale_info
				}
				)
				
			# Записываем полученные данные csv файл
			with open(f"data4/data_{cur_date}.csv", "a", encoding="utf-8") as file:
				writer = csv.writer(file)

				writer.writerow(
					(
						name,
						currency,
						twitter,
						starts_in_date,
						sale_info
						)
					)

		print(f"[INFO] Обработана страница {page}/9")

	# Записываем данные в json файл
	with open(f"data4/data_{cur_date}.json", "a") as file:
		json.dump(data, file, indent=4)

				
			



def main():
	pages_count = get_all_pages("https://coinmarketcap.com/nft/upcoming/")
	get_data(pages_count=pages_count)


if __name__ == '__main__':
	main()