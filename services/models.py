import json 

class Product():
	def __init__(self, title:str, image:str, price:str, description:str, catalog:str) -> None:
		self.title = title.strip()
		self.image = image.strip()
		self.price = price.strip()
		self.description = description.strip()
		self.catalog = catalog.strip()
	def __str__(self):
		return f"{self.title, self.image, self.price, self.description}"

class User ():
	def __init__(self, token:str, name:str, family:str, birthday:str, phone:str, email:str, login:str, password:str, image="https://png.pngtree.com/thumb_back/fh260/background/20230612/pngtree-in-the-style-of-2d-game-art-image_2884743.jpg"):
		self.token = token
		self.name = name
		self.family = family
		self.birthday = birthday
		self.phone = phone
		self.email = email
		self.login = login
		self.password = password
		self.image = image
		
	def to_dict(self) -> dict:
		return {
			"token":self.token,
			"name":self.name,
			"family":self.family,
			"birthday":self.birthday,
			"phone":self.phone,
			"email":self.email,
			"login":self.login,
			"passwrod":self.password,
			"image":self.image
		}


class Config():
	def __init__(self, namefile:str) -> None:
		self.namefile = namefile
		self.update_data()
		
	def update_data(self):
		try:
			with open(self.namefile, 'r', encoding='utf-8') as file:
				self.data = json.load(file)
		except json.decoder.JSONDecodeError:
			with open(self.namefile, 'w', encoding='utf-8') as file:
				file.write("[]")
				self.data = []

	def to_dict(self) -> dict:
		return self.data
		
	def to_str(self) -> str:
		with open(self.namefile, "r", encoding='utf-8') as temp_file: return temp_file.read()

	def get(self, key:str) -> str:
		return f"{self.data[key]}"

	def rewrite_from_form(self, str_data:str) -> None:
		dict_data = json.loads(str_data)
		with open(self.namefile, 'w', encoding='utf-8') as f:
			json.dump(dict_data, f, ensure_ascii=False, indent=4)

	def rewrite_from_str(self, str_data:str) -> None:
		dict_data = json.loads(str_data)
		with open(self.namefile, 'w', encoding='utf-8') as f:
			json.dump(dict_data, f, ensure_ascii=False, indent=4)

	def rewrite_from_dict(self, dict_data:dict) -> None:
		with open(self.namefile, 'w', encoding='utf-8') as f:
			json.dump(dict_data, f, ensure_ascii=False, indent=4)

	def resave(self) -> None:
		with open(self.namefile, 'w', encoding='utf-8') as f:
			json.dump(self.data, f, ensure_ascii=False, indent=4)

	def rewrite_user_category(self, id_user:str, category:str) -> None:
		c = 0
		for user in self.data:
			if str(self.data[c]["chat_id"]) == str(id_user):
				self.data[c]["category"] = category
				self.resave()
				self.rewrite_from_dict(self.data)
			c+=1

class Settings():
	def __init__(self, conf:Config):
		self.conf = conf
		self.dict_settings_values = {}
	def resave_values(self) -> None:
		self.conf.rewrite_from_dict(self.dict_settings_values)
