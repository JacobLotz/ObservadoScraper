from classes import *

class TestScrapeBase:

	def setup_method(self, method):
		print(f"Setting up {method}")

		self.base = ScrapeBase("https://waarneming.nl/observation/344360732/")
		self.base.chrome_options.add_argument("--headless")


	def teardown_method(self, method):
		print(f"Tearing down {method}")


	def test_SetParam(self):
		self.base.SetParam()
		assert True


	def test_CreateWebDriver(self):
		self.base.CreateWebDriver()
		self.base.CloseWebDriver()
		assert True


	def test_GetSoup(self):
		self.base.CreateWebDriver()
		self.base.GetSoup()
		self.base.CloseWebDriver()
		assert True
