from flask import Flask, request, render_template
from parser_service import *

class WebApp():
	def __init__(self) -> None:
		self.app = Flask(__name__)
		self.setup_routes()

	def setup_routes(self):
		@self.app.route('/')
		def index():
			return render_template('home.html')
	
	def start_app(self):
		self.app.run(debug=False)

def main() -> None:
	webapp = WebApp()
	webapp.start_app()

if __name__ == "__main__":
	main()
