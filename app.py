from flask import Flask, request, render_template, make_response, redirect
from services import parser, models

import redis, random
from services.models import Settings, Config, User


class ManagerRedis():
	def __init__(self):
		self.cursor = redis.Redis("127.0.0.1", 6379, 0)

	def set(self, key:str, value:any) -> None:
		self.cursor.set(key, value)

	def set_user(self, user:User) -> None:
		self.set(user.token, user.to_dict())

class ManagerCookies():
	def __init__(self, cursor:redis.Redis):
		self.cursor = cursor

	def is_match_cookies(self) -> bool:
		if len(request.cookies.keys()) == 0:
			return False
		return True
	
	def set_cookies_auth(self, dict_data_user:dict) :
		frm = dict_data_user
		token = self.init_token_str()
		response = redirect("/settings")
		print(f"RESPONSE RESULT:{response}")

		user = User(
			token,
			frm['name'], 
			frm['family'], 
			frm['birthday'], 
			frm['phone'], 
			frm['email'], 
			frm['telegram'], 
			frm['login'], 
			frm['password'],
			"https://png.pngtree.com/thumb_back/fh260/background/20230612/pngtree-in-the-style-of-2d-game-art-image_2884743.jpg")

		for k,v in user.to_dict():
			response.set_cookie(k,v)

		copy_dict_data_user = dict_data_user
		copy_dict_data_user["settings_pic_profile"] = "https://png.pngtree.com/thumb_back/fh260/background/20230612/pngtree-in-the-style-of-2d-game-art-image_2884743.jpg"
		self.cursor.hmset(token, copy_dict_data_user)
		return response

	def init_token_str(self) -> str:
		token = random.randint(100_000, 999_999)
		return str(token)
	


class WebApp():
	def __init__(self) -> None:
		self.conf = Config("config.json")
		self.mng_redis = ManagerRedis()
		self.mng_cookies = ManagerCookies(self.mng_redis.cursor())
		self.app = Flask(__name__)
		self.service_parser = parser.Parser()
		self.active_number_page = 1
		self.collection_products = self.service_parser.get_products(parser.URL_SALES["АКЦИИ"][0])
		self.setup_routes()

		self.settings = Settings(self.conf)
		self.settings.dict_settings_values = self.conf.data
		

	def get_active_index_collection(self) -> int:
		return self.active_number_page * int(self.settings.dict_settings_values['count_cards_in_page'])

	def edit_price_for_products(self, products:list[models.Product]) -> list[models.Product]:
		for product in products:

			product.price = float(product.price)
			product.price += (float(product.price) / 100) * float(self.settings.dict_settings_values['percent_plus_price'])
			product.price = float(product.price)+float(self.settings.dict_settings_values['num_plus_price'])

			product.price = str(round(product.price, 2))
		return products
			

	def get_slice_collection_for_page(self, collect:list[models.Product]) -> list[models.Product]:
		if self.active_number_page >= len(collect) or self.active_number_page < 0:
			return collect[:int(self.settings.dict_settings_values['count_cards_in_page'])]
		if len(collect) <= self.active_number_page * int(self.settings.dict_settings_values['count_cards_in_page']): 
			return collect[:int(self.settings.dict_settings_values['count_cards_in_page'])]

		if len(collect) <= self.active_number_page * int(self.settings.dict_settings_values['count_cards_in_page']) + int(self.settings.dict_settings_values['count_cards_in_page']):
			return collect[self.get_active_index_collection():]
		else:
			return collect[self.get_active_index_collection():self.get_active_index_collection()+int(self.settings.dict_settings_values['count_cards_in_page'])]



	def render_products(self, key:str, category:str) -> str:
		for temp_tab in parser.URL_DIRS:
			for key, value in temp_tab.items():
				if value[1] == category:
					return render_template(
							'products.html',
							settings = self.settings,
							array_products = self.get_slice_collection_for_page(self.edit_price_for_products(
								self.service_parser.get_products(
									temp_tab[key][0]
									)
								)),
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
			self.settings.dict_settings_values = self.conf.data
			return self.render_products("",category)
		@self.app.route('/')
		def route_products():
			self.settings.dict_settings_values = self.conf.data
			return self.render_products("","smartfony")

		@self.app.route('/settings')
		def route_settings():
			# self.settings.dict_settings_values = self.conf.data
			cookies_token = request.cookies.get('token')
			print(cookies_token)
			temp_data = self.mng_redis.cursor.hgetall(cookies_token)
			# temp_data = {temp_data}
			print("TEMP DATA FROM REDIS FOR TOKEN",temp_data)
			self.settings.dict_settings_values = temp_data
			return render_template('settings.html', settings=self.settings)

		@self.app.route('/settings_apply', methods=['POST'])
		def route_settings_apply():
			form_settings = request.form
			for field in form_settings:
				self.settings.dict_settings_values[field] = form_settings[field]
			self.conf.rewrite_from_dict(self.settings.dict_settings_values)
			return render_template('settings.html', settings=self.settings)

		@self.app.route('/support')
		def route_support():
			return render_template('support.html')

		@self.app.route('/orders')
		def route_orders():
			return render_template('orders.html')

		@self.app.route('/next')
		def route_next():
			self.active_number_page += 1
			return render_template('orders.html')

		@self.app.route('/prev')
		def route_prev():
			self.active_number_page -= 1
			if self.active_number_page < int(len(self.collection_products) / int(int(self.settings.dict_settings_values['count_cards_in_page']))):
				self.active_number_page += 1
			return render_template('orders.html')

		@self.app.route('/login')
		def route_login():
			return render_template('login.html')
	
		@self.app.route('/auth', methods=['POST'])
		def route_cookies():
			self.settings.dict_settings_values = self.conf.data
			if self.mng_cookies.is_match_cookies() == False:
				temp_data = {}
				return self.mng_cookies.set_cookies_auth(temp_data)
			
			return redirect('/registration')

		@self.app.route('/registration')
		def route_registration():
			return render_template('registration.html')

		@self.app.route('/registration_apply', methods=['POST'])
		def route_registration_apply():
			temp_data = {}
			form_registration = request.form
			for field in form_registration:
				temp_data[field] = form_registration[field]
				
			print(temp_data)
			self.mng_redis.set_user()
			response_redirect_settings = self.mng_cookies.set_cookies_auth(temp_data)
			return response_redirect_settings

	def start_app(self) -> None:
		self.app.run(debug=False)


def main() -> None:
	webapp = WebApp()
	webapp.start_app()

if __name__ == "__main__":
	main()
