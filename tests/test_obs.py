
from classes import *


class TestObservation:

	def setup_method(self, method):
		print(f"Setting up {method}")

		self.obscollink = "https://waarneming.nl/users/41541/observations/?date_after=2025-04-11&date_before=2025-04-12&species_group=&rarity=&search=&advanced=on&species=&sex=&month=&country_division=&life_stage=&activity=&method=&validation_status="
		self.obscol = ObsCollection(self.obscollink)
		self.obscol.chrome_options.add_argument("--headless")
		self.obscol.CreateWebDriver()

		self.obs = Observation("https://waarneming.nl/observation/344360732/", self.obscol.browser)



	def teardown_method(self, method):
		print(f"Tearing down {method}")


	def test_GetData(self):
		self.obs.GetData()

		assert self.obs.Year == "2025"
		assert self.obs.Month == "04"
		assert self.obs.Day == "12"
		assert self.obs.Latitude == "52.1398"
		assert self.obs.Longitude == "6.0858"
