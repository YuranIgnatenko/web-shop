class Product():
	def __init__(self, title:str, image:str, price:str, description:str) -> None:
		self.title = title.strip()
		self.image = image.strip()
		self.price = price.strip().replace(r"\xa", "")
		self.description = description.strip()
	def __str__(self):
		return f"{self.title, self.image, self.price, self.description}"

