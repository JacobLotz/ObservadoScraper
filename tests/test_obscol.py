from classes import *
import time

from selenium import webdriver
from selenium.webdriver.common.by import By

class TestObsCollection:

	def setup_method(self, method):
		print(f"Setting up {method}")

		self.testlink = "https://waarneming.nl/users/41541/observations/?date_after=2025-04-11&date_before=2025-04-12&species_group=&rarity=&search=&advanced=on&species=&sex=&month=&country_division=&life_stage=&activity=&method=&validation_status="
		self.obscol = ObsCollection(self.testlink)
		self.obscol.chrome_options.add_argument("--headless")
		self.obscol.CreateWebDriver()


	def teardown_method(self, method):
		print(f"Tearing down {method}")
		self.obscol.CloseWebDriver()


	def test_SetName(self):
		self.obscol.SetName("test.kml")
		assert self.obscol.Name == "test.kml"

	def test_GetObservations(self):
		self.obscol.SetLang()
		time.sleep(1)
		self.obscol.GetObservations()

		assert len(self.obscol.Obs) == 6
		assert self.obscol.Obs[0] == "/observation/344360732/"
		