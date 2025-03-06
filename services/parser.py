import requests
from bs4 import BeautifulSoup
import sys, json, argparse

import services.models as models

URL_DIRS = {
	"НОУТБУКИ":"https://skypka.com/katalog/kompyuternaya-tekhnika/noutbuki-i-netbuki/?PAGEN_1=",
	"МОНИТОРЫ":"https://skypka.com/katalog/kompyuternaya-tekhnika/monitory/?PAGEN_1=",
	"СИСТЕМНЫЕ БЛОКИ":"https://skypka.com/katalog/kompyuternaya-tekhnika/sistemnye-bloki/",
	"ПЛАНШЕТЫ":"https://skypka.com/katalog/kompyuternaya-tekhnika/planshety/",
	"МФУ":"https://skypka.com/katalog/kompyuternaya-tekhnika/mfu_print/",
	"МОНОБЛОКИ":"https://skypka.com/katalog/kompyuternaya-tekhnika/monobloki/",

	"СМАРТФОНЫ":"https://skypka.com/katalog/telefony-i-aksessuary/smartfony/",
	"СМАРТ-ЧАСЫ":"https://skypka.com/katalog/telefony-i-aksessuary/smart-chasy/",
	"ВИРТУАЛЬНЫЕ ОЧКИ":"https://skypka.com/katalog/telefony-i-aksessuary/virtualnye-ochki/",
	"ФИТНЕС БРАСЛЕТЫ":"https://skypka.com/katalog/telefony-i-aksessuary/fitnes-braslety/",
	"ЭЛЕКТРОННЫЕ КНИГИ":"https://skypka.com/katalog/telefony-i-aksessuary/elektronnye-knigi/",
	"ЭКШН-КАМЕРЫ":"https://skypka.com/katalog/telefony-i-aksessuary/ekshn-kamery/",

	"АКЦИИ":"https://skypka.com/katalog/sales/",

}

URL_PREFIX_IMAGE = "https://skypka.com"



class Parser():
	def __init__(self) -> None:
		self.headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
		self.cookies  = {}

	def build_url(self, category:str, number_page:int) -> str:
		return URL_DIRS[category]+f"{number_page}"
	
	def get_soup(self, url:str) -> BeautifulSoup:
		response = requests.get(url, headers=self.headers, cookies=self.cookies)
		soup = BeautifulSoup(response.text, 'html.parser')
		return soup

	def get_count_pages(self, url:str) -> int:
		soup = self.get_soup(url)
		num = soup.find("div",class_="bx-pagination-container").find_all("span")[-2].text
		return int(num)		
	
	def get_count_products(self, url:str) -> int:
		soup = self.get_soup(url)
		num = soup.find("div",class_="catalog__all-goods catalog__all-goods_bottom").text.replace("Всего", "").replace("товаров", "").strip()
		return int(num)		

	def get_products(self, url:str) -> list[ models.Product ]:
		soup = self.get_soup(url)
		temp_array_products = []
		for div in soup.find_all("div", class_="product-card-item"):
			title = div.find("a", class_="product-card-item__link link").text
			price = div.find("div", class_="product-card-item__prices").find("p").text
			image = URL_PREFIX_IMAGE + div.find("a",class_="product-card-item__image").find("img").get("src")
			description = div.find("p", class_="product-card-item__description").text
			temp_array_products.append(models.Product(title, image, price, description))
		return temp_array_products


def main() -> None:
	def test():
		parser = Parser()
		ar_prods = parser.get_products(self.build_url("НОУТБУКИ",1))
		print(parser.get_count_pages(self.build_url("НОУТБУКИ",1)))
		print(parser.get_count_products(self.build_url("НОУТБУКИ",1)))

		for i in ar_prods:
			print(i)

	test()

if __name__ == "__main__":
	main()