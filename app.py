from flask import Flask, request, render_template
from services import parser, models
from config import Config

class Settings():
	def __init__(self, conf:Config):
		self.conf = conf
		self.dict_settings_values = {}
	def resave_values(self) -> None:
		self.conf.rewrite_from_dict(self.dict_settings_values)


class WebApp():
	def __init__(self) -> None:
		self.conf = Config("config.json")
		self.app = Flask(__name__)
		self.service_parser = parser.Parser()
		self.collection_products = self.service_parser.get_products(parser.URL_SALES["АКЦИИ"][0])
		self.setup_routes()

		self.settings = Settings(self.conf)
		

	def edit_price_for_products(self, products:list[models.Product]) -> list[models.Product]:
		for product in products:
			product.price = float(product.price)+float(self.settings.num_plus_price) + 100/float(self.settings.percent_plus_price)
			product.price = str(round(product.price, 2))
		return products
			


	def render_products(self, key:str, category:str) -> str:
		for temp_tab in parser.URL_DIRS:
			for key, value in temp_tab.items():
				if value[1] == category:
					return render_template(
							'products.html',
							array_products = self.edit_price_for_products(
								self.service_parser.get_products(
									temp_tab[key][0]
									)
								),
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

		@self.app.route('/settings_apply', methods=['POST'])
		def route_settings_apply():
			form_settings = request.form
			# self.settings.dict_settings_values = {}
			for field in form_settings:
				self.settings.dict_settings_values[field] = form_settings[field]
				print(field, form_settings[field])
			self.conf.rewrite_from_dict(self.settings.dict_settings_values)
			# self.settings.resave_values()
			return render_template('settings.html', settings=self.settings)

		@self.app.route('/support')
		def route_support():
			return render_template('support.html')

		@self.app.route('/orders')
		def route_orders():
			return render_template('orders.html')

	def start_app(self) -> None:
		self.app.run(debug=False)


def main() -> None:
	webapp = WebApp()
	webapp.start_app()

if __name__ == "__main__":
	main()
