import requests
from bs4 import BeautifulSoup
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service



	
def get_data_with_selenium(url):
    count = 0
    
    # ЗАХОДИМ В САЙТ КАК ПОЛЬЗОВАТЕЛЬ С SELENIUM

   # try:
   # 	s = Service('C:/Users/Admin/Desktop/chromedriver.exe')
   # 	driver = webdriver.Chrome(service=s)
   # 	driver.get(url=url)
   # 	time.sleep(10)

    #	with open("index_selenium.html", "w") as file:
    #		file.write(driver.page_source)

    # except Exception as ex:
    #	print(ex)

    with open("index_selenium.html") as file:
    	src =file.read()

    soup = BeautifulSoup(src, 'lxml')

    name_list = []
    paids_dict = {}

    # Парсим...
    table = soup.find("div", class_="table-placeholder").find(class_="table").find("tbody")
    tr_all = table.find_all("tr")
    for tr in tr_all:
        num = tr.find("td").find_next().text
        name = tr.find("td").text
        paids_dict[name] = num

        count += 1
        time.sleep(0.5)
        print(f"#{count}")

    # Добавляем словарь в список
    name_list.append(paids_dict)

    # Сохроняем данные в json файл
    with open("result.json", "w", encoding="utf-8") as json_file:
        json.dump(name_list, json_file, indent=4, ensure_ascii=False)



def main():
	get_data_with_selenium("http://stat.sakha.gks.ru/page.aspx?s=ias&m=7589&p=4065")

if __name__ == '__main__':
	main()