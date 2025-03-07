from flask import Flask, request, render_template
from services import parser, models
from config import Config

class Settings():
	def __init__(self, conf:Config):
		self.percent_plus_price = conf.get("percent_plus_price")
		self.num_plus_price = conf.get("num_plus_price")
		self.period_parsing = conf.get("period_parsing")
		self.count_cards_in_page = conf.get("count_cards_in_page")


class WebApp():
	def __init__(self) -> None:
		self.conf = Config("config.json")
		self.app = Flask(__name__)
		self.service_parser = parser.Parser()
		self.collection_products = self.service_parser.get_products(parser.URL_SALES["АКЦИИ"][0])
		self.setup_routes()

		self.settings = Settings(self.conf)
		

	def render_products(self, key:str, category:str) -> str:
		for temp_tab in parser.URL_DIRS:
			for key, value in temp_tab.items():
				if value[1] == category:
					return render_template(
							'products.html',
							array_products = self.service_parser.get_products(temp_tab[key][0]),
							tab_1 = parser.URL_PC,
							tab_2 = parser.URL_GAJET,
							tab_3 = parser.URL_PHOTO_AUDIO,
							tab_4 = parser.URL_INSTRUMENT,
							tab_5 = parser.URL_OTHERS,				
							tab_6 = parser.URL_SALES,
							)
		return self.render_products("","smartfony")


	def setup_routes(self):
		@self.app.route('/<category>')
		def route_a(category):
			return self.render_products("",category)
		@self.app.route('/')
		def route_products():
			return self.render_products("","smartfony")

		@self.app.route('/settings')
		def route_settings():
			return render_template('settings.html', settings=self.settings)

		@self.app.route('/orders')
		def route_orders():
			return render_template('orders.html')


	def start_app(self):
		self.app.run(debug=False)

def main() -> None:
	webapp = WebApp()
	webapp.start_app()

if __name__ == "__main__":
	main()
