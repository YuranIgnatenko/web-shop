from flask import Flask, request, render_template
from services import parser, models

class WebApp():
	def __init__(self) -> None:
		self.app = Flask(__name__)
		self.service_parser = parser.Parser()
		self.collection_products = self.service_parser.get_products(parser.URL_DIRS["НОУТБУКИ"])
		self.setup_routes()

	def setup_routes(self):
		@self.app.route('/products')
		def index():
			return render_template(
				'products.html',
				email="test@test.com",
				Phone="8989898989898",
				Location_office="office_test",
				Copyright="2025",
				IsLogin=True,
				NameLogin="Admin",
				IsAdmin=True,
				array_products=self.collection_products,

				)
	
	def start_app(self):
		self.app.run(debug=False)

def main() -> None:
	webapp = WebApp()
	webapp.start_app()

if __name__ == "__main__":
	main()
