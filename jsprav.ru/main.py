import os
import requests
from bs4 import BeautifulSoup

def get_data():

    url = "https://smolensk.jsprav.ru/"

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
        "accept": "*/*"
    }

    r = requests.get(url=url, headers=headers)
    #print(r.text)

    if not os.path.exists("data"):
        os.mkdir("data")

    #with open("data/index.html", "w", encoding="utf-8") as file:
        #file.write(r.text)

    with open("data/index.html", "r", encoding="utf-8") as file:
        src = file.read()

    data = []

    # собираем все ссылки категории
    soup = BeautifulSoup(src, 'lxml')
    columns = soup.find_all("div", class_="cat-tile__blc")
    for column in columns:

        if column.find("dl", class_="cat-tile__blc-list"):
            cats = column.find("dl", class_="cat-tile__blc-list").find_all("dt", class_="cat-tile__blc-list-name")
            for cat in cats:
                title_cat = cat.find("a").text
                link_cat = cat.find("a").get("href")
                url_cat = f"https://smolensk.jsprav.ru{link_cat}"

                # собираем информацию с полученных ссылок
                r = requests.get(url=url_cat)

                soup = BeautifulSoup(r.text, 'lxml')
                cards = soup.find("ul", class_="company-list").find_all("div", class_="company-list__i-data")
                for card in cards:
                    title = card.find("span", class_="company-info-name-org").text
                    category = card.find("span", class_="company-info-name-category").text
                    address = card.find("address").text.strip()
                    time_work = card.find("span", class_="company-info-time-full company-info-text")
                    phone_number = card.find("span", class_="company-info-phone-number")
                    print(time_work, title)

                    data.append({
                            "Название " : title,
                            "Категория " : category,
                            "Адресс " : address,
                            "Телефон " : phone_number,
                            "Время работы " : time_work
                        })
           
            title_column = column.find("h3").text

            print(title)


def main():
    get_data()

if __name__ == "__main__":
    main()
