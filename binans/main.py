import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import datetime
import time
import json
import os

start_time = time.time()

def get():
	url = "https://www.binance.com/ru/markets/spot-USDT"

	headers = {
	"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
	"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
	}

	r = requests.get(url=url, headers=headers)

	if not os.path.exists("data"):
		os.mkdir("data")

	with open("data/index_1.html", "w", encoding="utf-8") as file:
		file.write(r.text)

	soup = BeautifulSoup(r.text, 'lxml')

	pages = int(soup.find("div", class_="css-b0tuh4").find_all("button", class_="css-hlqxzb")[-1].text)
	for page in range(2, pages+1):

		try:
				driver = webdriver.Chrome(executable_path="C:\\Users\\Admin\\Desktop\\chromedriver.exe")
				driver.get(url=url)
				time.sleep(5)

				button_cuci = driver.find_element_by_id("onetrust-accept-btn-handler").click()
				time.sleep(5)
				button = driver.find_elements_by_class_name("css-hlqxzb")[page-2].click()
				time.sleep(5)

				with open(f"data/index_{page}.html", "w", encoding="utf-8") as file:
					file.write(driver.page_source)
			
		except Exception as ex:
			print(ex)
		finally:
			driver.close()
			driver.quit()

	for page in range(1, pages+1):

		with open(f"data/index_{page}.html", "r", encoding="utf-8") as file:
			src = file.read()

		# get data
		data = []

		soup = BeautifulSoup(src, "lxml")
		cards = soup.find_all("div", class_="css-vlibs4")
		for card in cards:
			title = card.find("div", class_="css-14yoi5o").find("a", class_="css-1sud65k").text
			price = card.find("div", class_="css-10nf7hq").find("div").text.strip()
			try:
				changes = card.find("div", class_="css-1vefg8").text
			except:
				changes = card.find("div", class_="css-131bcdq").text
			maxmin = card.find("div", class_="css-102bt5g").text.split("/")
			max24h = maxmin[0].strip()
			min24h = maxmin[1].strip()
			volume = card.find("div", style="width:130px;flex:130;direction:ltr").text
			capit = card.find_all("div", class_="css-102bt5g")[-1].text
			#print(title)

			data.append({
				"Название" : title,
				"Цена" : price,
				"Изм за 24ч" : changes,
				"Макс 24ч" : max24h,
				"Мин за 24ч" : min24h,
				"Объем за 24ч" : volume,
				"Капитализация" : capit
				})

			with open(f"data/data_{page}.json", "w", encoding="utf-8") as file:
				json.dump(data, file, indent=4, ensure_ascii=False)


def main():
	get()
	finish_time = time.time() - start_time
	print(f"Затраченное на работу скрипта время: {finish_time}")

if __name__ == '__main__':
	main()