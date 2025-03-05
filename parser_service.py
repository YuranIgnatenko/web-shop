import requests
from bs4 import BeautifulSoup
import sys, json, argparse

URL_STRONILUM = "TEST"

class MissingPeople():
	def __init__(self, title:str, url_image:str, date_create:str, url_html_page:str, description:str, id:str) -> None:
		self.url_image = url_image
		self.date_create = date_create 
		self.url_html_page = url_html_page
		self.description =  description
		self.title = title
		self.id = id
	def get_id(self):
		return self.url_html_page.split("/")[-2]


def MissingPeopleFromSoup(url_site_prefix:str, soup_section:BeautifulSoup) -> MissingPeople:

	try:
		temp_title = soup_section.find("div", class_="bl-item-holder").find("div", class_="bl-item-title").find("a").text
	except:
		temp_title = soup_section.find("div", class_="bl-item-holder").find("div", class_="bl-item-title").find("a").text

	try:
		url_image = URL_SITE_SLEDCOM+soup_section.find("div", class_="bl-item-image").find("a").find("img").get("src")
	except:
		url_image = "/static/img/alert.jpg"

	try:
		description = soup_section.find("div", class_="bl-item-holder").find("div", class_="bl-item-text")
		description = "\n".join([t.find("span").text for t in description.find_all("p")])
	except:
		description = soup_section.find("div", class_="bl-item-holder").find("div", class_="bl-item-text")
		description = "\n".join([t.text for t in description.find_all("p")])

	try:
		url_html_page = soup_section.find("div", class_="bl-item-title").find("a").get("href")
	except:
		url_html_page = soup_section.find("div", class_="bl-item-title").find("a").get("href")


	id = f"{url_html_page.split("/")[-2]}"

	return MissingPeople(temp_title, url_image,temp_title,url_html_page,description, id)


class ParserMvd():
	def __init__(self) -> None:
		self.headers = { 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'}
		self.cookies  = {}

	def get_array_people(self, url:str) -> list[str]:
		response = requests.get(url, headers=self.headers, cookies=self.cookies)
		soup = BeautifulSoup(response.text, 'html.parser')
		
		temp_array_peoples = []

		for div in soup.find('div', class_="section-list type-10 m-t3 m-b2").find("div", class_="sl-holder").find_all("div", class_="sl-item"):
			url_image =  "http:"+div.find("div", class_="sl-item-image").find("a", class_="e-popup_html").find("img").get("src")
			name = div.find("div", class_="sl-item-title").find("a", class_="e-popup_html").text
			temp_array_peoples.append(MissingPeople(name, url_image,"no",url, "Розыск !", name.replace(" ", "")))

		return temp_array_peoples



def main() -> None:
	def test_sledkom():
		parser = ParserSledcom()
		ar1 = parser.get_array_people(DICT_URLS_SLEDCOM["БЕЗ ВЕСТИ"])
		for people in ar1:
			print("GET ARRAY PEOPLE",people.date_create, people.url_image, people.description)

	def test_mvd():
		parser = ParserMvd()
		parser.get_array_people(URL_SITE_MVD)

	def test_liza_alert():
		parser = ParserLizaAlert()
		parser.get_array_people(URL_SITE_LIZAALERT)

	# test_sletkom()
	# test_mvd()
	test_liza_alert()

if __name__ == "__main__":
	main()