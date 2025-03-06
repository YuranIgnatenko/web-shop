from flask import Flask, request, render_template
from services import parser, models

class WebApp():
	def __init__(self) -> None:
		self.app = Flask(__name__)
		self.service_parser = parser.Parser()
		self.collection_products = self.service_parser.get_products(parser.URL_DIRS["АКЦИИ"]["АКЦИИ"])
		self.setup_routes()

	def render_products(self, name_category:str, key_category:str) -> str:
		return render_template(
				'products.html',
				array_products = self.service_parser.get_products(parser.URL_DIRS[name_category][key_category]),
				tab_1 = parser.URL_DIRS['ГАДЖЕТЫ'],
				tab_2 = parser.URL_DIRS['ЭЛЕТРОНИКА'],
				tab_3 = parser.URL_DIRS['ИНСТРУМЕНТЫ'],
				tab_4 = parser.URL_DIRS['ФОТОАУДИОТЕХНИКА'],
				tab_5 = parser.URL_DIRS['ПРОЧЕЕ'],				
				tab_6 = parser.URL_DIRS['АКЦИИ'],
				)

	def setup_routes(self):
		@self.app.route('/products')
		def route_products():
			return self.render_products("АКЦИИ","АКЦИИ")

		@self.app.route('/noutbuki')
		def route_noutbuki():
			return self.render_products("НОУТБУКИ")

		@self.app.route('/monitori')
		def route_monitori():
			return self.render_products("МОНИТОРЫ")
				
		@self.app.route('/sistemniebloki')
		def route_sistemniebloki():
			return self.render_products("СИСТЕМНЫЕ БЛОКИ")



	def start_app(self):
		self.app.run(debug=False)

def main() -> None:
	webapp = WebApp()
	webapp.start_app()

if __name__ == "__main__":
	main()
