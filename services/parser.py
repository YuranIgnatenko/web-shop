import requests
from bs4 import BeautifulSoup
import sys, json, argparse

import services.models as models

URL_DIRS = {
	"НОУТБУКИ":"https://skypka.com/katalog/kompyuternaya-tekhnika/noutbuki-i-netbuki/",
	"МОНИТОРЫ":"https://skypka.com/katalog/kompyuternaya-tekhnika/monitory/",
	"СИСТЕМНЫЕ БЛОКИ":"https://skypka.com/katalog/kompyuternaya-tekhnika/sistemnye-bloki/",
	"МФУ":"https://skypka.com/katalog/kompyuternaya-tekhnika/mfu_print/",
	"МОНОБЛОКИ":"https://skypka.com/katalog/kompyuternaya-tekhnika/monobloki/",

	"СМАРТФОНЫ":"https://skypka.com/katalog/telefony-i-aksessuary/smartfony/",
	"ПЛАНШЕТЫ":"https://skypka.com/katalog/kompyuternaya-tekhnika/planshety/",
	"СМАРТ-ЧАСЫ":"https://skypka.com/katalog/telefony-i-aksessuary/smart-chasy/",
	"ЧАСЫ":"https://skypka.com/katalog/chasy/",
	"ВИРТУАЛЬНЫЕ ОЧКИ":"https://skypka.com/katalog/telefony-i-aksessuary/virtualnye-ochki/",
	"ФИТНЕС БРАСЛЕТЫ":"https://skypka.com/katalog/telefony-i-aksessuary/fitnes-braslety/",
	"ЭЛЕКТРОННЫЕ КНИГИ":"https://skypka.com/katalog/telefony-i-aksessuary/elektronnye-knigi/",
	"ЭКШН-КАМЕРЫ":"https://skypka.com/katalog/telefony-i-aksessuary/ekshn-kamery/",

	"ТОВАРЫ ДЛЯ САДА":"https://skypka.com/katalog/instrument/ruchnoy-instrument/",
	"ЭЛЕКТРОИНСТРУМЕНТ":"https://skypka.com/katalog/instrument/elektroinstrument/",
	"ИЗМЕРИТЕЛИ":"https://skypka.com/katalog/instrument/izmeritelnie-instrumenti/",
	"СИЛОВАЯ ТЕХНИКА":"https://skypka.com/katalog/instrument/silovaya-tekhnika/",
	"СТАНКИ":"https://skypka.com/katalog/instrument/zatochnye-stanki-tochila/",

	"АУДИОТЕХНИКА":"https://skypka.com/katalog/tv-i-video/audiotekhnika/",
	"ПЛЕЕРЫ, DVD":"https://skypka.com/katalog/tv-i-video/dvd-blu-ray-pleery/",
	"АКСЕССУАРЫ ДЛЯ ФОТО И ВИДЕО":"https://skypka.com/katalog/tv-i-video/aksessuary-dlya-foto-i-video/",
	"ДОМАШНИИ КИНОТЕАТРЫ":"https://skypka.com/katalog/tv-i-video/domashnie-kinoteatry/",
	"МИКРОФОНЫ":"https://skypka.com/katalog/tv-i-video/mikrofony/",
	"ДЛЯ ТЕЛЕВИЗОРА":"https://skypka.com/katalog/tv-i-video/sputnikovoe-i-tsifrovoe-tv/",
	"ТЕЛЕВИЗОРЫ":"https://skypka.com/katalog/tv-i-video/televizory/",
	"ТЕХНИКА HI-FI":"https://skypka.com/katalog/tv-i-video/tekhnika-hi-fi/",
	"ФОТОАППАРАТЫ И ОБЪЕКТИВЫ":"https://skypka.com/katalog/tv-i-video/fotoapparaty-i-obektivy/",
	"ПРОЕКТОРЫ И ЭКРАНЫ":"https://skypka.com/katalog/tv-i-video/proektory-i-ekrany/",
	"ФОТОАППАРАТЫ И АКСЕССУАРЫ":"https://skypka.com/katalog/tv-i-video/fotoapparaty-i-fototekhnika/",
	"ВИДЕОКАМЕРЫ":"https://skypka.com/katalog/tv-i-video/videokamery/",

	"ШУБЫ":"https://skypka.com/katalog/shuby/",
	
	"БАРБЕКЮ И ГРИЛИ":"https://skypka.com/katalog/bytovaya-tekhnika/barbekyu-i-grili/",
	"КОФЕМАШИНЫ":"https://skypka.com/katalog/bytovaya-tekhnika/kofemashiny/",

	"АККАРДЕОНЫ И БАЯНЫ":"https://skypka.com/katalog/muzykalnoe-oborudovanie/akkordeony/",
	"ГИТАРЫ":"https://skypka.com/katalog/muzykalnoe-oborudovanie/gitari/",
	"ДУХОВЫЕ ИНСТРУМЕНТЫ":"https://skypka.com/katalog/muzykalnoe-oborudovanie/dukhovye-instrumenty/",
	"КЛАВИШНЫЕ":"https://skypka.com/katalog/muzykalnoe-oborudovanie/klavishnye-instrumenty/",
	"ЛАЗЕРЫ И СЕТОТЕХНИКА":"https://skypka.com/katalog/muzykalnoe-oborudovanie/lazery-i-svetotekhnika/",	

	"СВОБОДНЫЕ ВЕСА":"https://skypka.com/katalog/sport-turizm-i-otdykh/svobodnye-vesa/",
	"СИЛОВЫЕ ТРЕНАЖЕРЫ":"https://skypka.com/katalog/sport-turizm-i-otdykh/silovye-trenazhery/",
	"ЗИМНИЙ СПОРТ":"https://skypka.com/katalog/sport-turizm-i-otdykh/tovary-dlya-zimnikh-vidov-sporta/",
	"ТОВАРЫ ДЛЯ РЫБАЛКИ":"https://skypka.com/katalog/sport-turizm-i-otdykh/tovary-dlya-rybalki/",

	"АВТОАККУСТИКА":"https://skypka.com/katalog/avtoaksessuary/avtoakustika/",
	"АВТОНАСОСЫ И КОМПРЕССОРЫ":"https://skypka.com/katalog/avtoaksessuary/avtomobilnye-nasosy-i-kompressory/",
	"АВТОЭЛЕКТРОНИКА":"https://skypka.com/katalog/avtoaksessuary/avtoelektronika/",
	"АВТО ЗУ":"https://skypka.com/katalog/avtoaksessuary/zaryadnye-ustroystva2/",
	"ШИНЫ И ДИСКИ":"https://skypka.com/katalog/avtoaksessuary/kolesa/",


	"PSP":"https://skypka.com/katalog/igrovye-pristavki/igrovaya-pristavka-psp/",
	"SEGA":"https://skypka.com/katalog/igrovye-pristavki/igrovaya-pristavka-sega/",
	"SONY PLAYSTATION":"https://skypka.com/katalog/igrovye-pristavki/igrovye-pristavki-sony-playstation/",
	"XBOX":"https://skypka.com/katalog/igrovye-pristavki/igrovye-pristavki-xbox/",
	"PSP VITA":"https://skypka.com/katalog/igrovye-pristavki/igrovaya-pristavka-psp-vita/",


	"АКЦИИ":"https://skypka.com/katalog/sales/",
	"ПРОЧЕЕ":"https://skypka.com/katalog/prochie-tovary/",

}

URL_PREFIX_IMAGE = "https://skypka.com"



class Parser():
	def __init__(self) -> None:
		self.headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
		self.cookies  = {}

	def build_url(self, category:str, number_page:int) -> str:
		return URL_DIRS[category] + f"?PAGEN_1={number_page}"
	
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
			price = div.find("div", class_="product-card-item__prices").find("p").text.replace("₽","").strip()
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