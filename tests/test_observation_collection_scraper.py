import os
from unittest.mock import Mock, patch
from bs4 import BeautifulSoup
from classes import ObservationCollectionScraper


class TestObservationCollectionScraper:
    """Tests for ObservationCollectionScraper using mocked HTML and browser"""

    def setup_method(self, method):
        print(f"Setting up {method}")
        self.test_dir = os.path.dirname(__file__)

    def _load_mock_html(self, filename):
        """Load mock HTML file and return BeautifulSoup object"""
        mock_file = os.path.join(self.test_dir, 'mocks', filename)
        with open(mock_file, 'r', encoding='utf-8') as f:
            html = f.read()
        return BeautifulSoup(html, 'html.parser')

    def test_get_observation_links(self):
        """Test extracting observation links from overview page"""
        scraper = ObservationCollectionScraper("https://waarneming.nl/observations/?page=1")

        # Mock the browser and page loading
        mock_browser = Mock()
        scraper.browser = mock_browser
        scraper.Wait = 0

        # Create a single page mock (no pagination)
        html_single_page = """
        <html>
            <div class="observations-list">
                <div class="observation-item">
                    <a href="/observation/382543115/">Obs 1</a>
                </div>
                <div class="observation-item">
                    <a href="/observation/382543116/">Obs 2</a>
                </div>
                <div class="observation-item">
                    <a href="/observation/382543117/">Obs 3</a>
                </div>
            </div>
        </html>
        """

        scraper.PageSoup = BeautifulSoup(html_single_page, 'html.parser')
        scraper.GetSoup = Mock()

        # Call the internal method
        links = scraper._get_observation_links()

        assert len(links) == 3
        assert "/observation/382543115/" in links
        assert "/observation/382543116/" in links
        assert "/observation/382543117/" in links

    def test_get_observation_links_filtered(self):
        """Test filtering observation links by species"""
        scraper = ObservationCollectionScraper("https://waarneming.nl/observations/?page=1")

        # Mock the browser
        mock_browser = Mock()
        scraper.browser = mock_browser
        scraper.Wait = 0

        # Create HTML with species names
        html_with_species = """
        <html>
            <div class="observations-list">
                <div class="observation-item">
                    <a href="/observation/1/">Obs 1</a>
                    <span class="species-common-name">Boswitje</span>
                </div>
                <div class="observation-item">
                    <a href="/observation/2/">Obs 2</a>
                    <span class="species-common-name">Gewone Zeehond</span>
                </div>
                <div class="observation-item">
                    <a href="/observation/3/">Obs 3</a>
                    <span class="species-common-name">Boswitje</span>
                </div>
                <div class="observation-item">
                    <a href="/observation/4/">Obs 4</a>
                    <span class="species-common-name">Andere Soort</span>
                </div>
            </div>
        </html>
        """

        scraper.PageSoup = BeautifulSoup(html_with_species, 'html.parser')
        scraper.GetSoup = Mock()

        # Filter for only Boswitje
        species_filter = {'Boswitje'}
        links = scraper._get_observation_links_filtered(species_filter)

        # Should only get 2 links (both Boswitje observations)
        assert len(links) == 2
        assert "/observation/1/" in links
        assert "/observation/3/" in links
        assert "/observation/2/" not in links
        assert "/observation/4/" not in links

    def test_save_and_load_csv(self):
        """Test the save and load functionality"""
        import tempfile
        import pandas as pd

        # Create test DataFrame
        test_data = {
            'name': ['Species 1', 'Species 2'],
            'datetime': ['2025-12-14 10:00', '2025-12-15 11:00'],
            'latitude': ['52.1', '52.2'],
            'longitude': ['4.1', '4.2']
        }
        df = pd.DataFrame(test_data)

        # Create temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_csv = f.name

        try:
            # Test save
            scraper = ObservationCollectionScraper("dummy_link")
            scraper.save(df, temp_csv)

            # Test load
            loaded_df = ObservationCollectionScraper.load(temp_csv)

            assert len(loaded_df) == 2
            assert list(loaded_df['name']) == ['Species 1', 'Species 2']
            # CSV loading converts numeric strings to floats
            assert float(loaded_df['latitude'][0]) == 52.1
        finally:
            import os
            if os.path.exists(temp_csv):
                os.unlink(temp_csv)

    @patch('classes.observation_collection_scraper.ObservationScraper')
    def test_scrape_with_mocked_observation_scraper(self, MockObsScraper):
        """Test full scrape workflow with mocked ObservationScraper"""
        # This tests the scraping without actually using Selenium

        scraper = ObservationCollectionScraper("https://waarneming.nl/observations/?page=1")

        # Mock browser and webdriver methods
        scraper.CreateWebDriver = Mock()
        scraper.CloseWebDriver = Mock()
        scraper.SetLang = Mock()
        scraper.browser = Mock()
        scraper.Wait = 0

        # Mock _get_observation_links to return test links
        scraper._get_observation_links = Mock(return_value=[
            "/observation/1/",
            "/observation/2/",
            "/observation/3/"
        ])

        # Mock ObservationScraper to return test data
        mock_obs_instance = Mock()
        MockObsScraper.return_value = mock_obs_instance

        # Return different data for each observation
        mock_obs_instance.scrape.side_effect = [
            {
                'name': 'Species 1',
                'datetime': '2025-12-14 10:00',
                'year': '2025',
                'month': '12',
                'day': '14',
                'month_day': '14-12',
                'time': '10:00',
                'location_name': 'Location 1',
                'latitude': '52.1',
                'longitude': '4.1',
                'description': 'Test 1',
                'url': 'https://waarneming.nl/observation/1/'
            },
            {
                'name': 'Species 2',
                'datetime': '2025-12-15 11:00',
                'year': '2025',
                'month': '12',
                'day': '15',
                'month_day': '15-12',
                'time': '11:00',
                'location_name': 'Location 2',
                'latitude': '52.2',
                'longitude': '4.2',
                'description': 'Test 2',
                'url': 'https://waarneming.nl/observation/2/'
            },
            None  # Observation 3 has no GPS (obscured)
        ]

        # Run scrape
        df = scraper.scrape()

        # Verify results
        assert len(df) == 2  # Only 2 observations (third was None)
        assert df['name'].tolist() == ['Species 1', 'Species 2']
        assert df['latitude'].tolist() == ['52.1', '52.2']

        # Verify methods were called
        scraper.CreateWebDriver.assert_called_once()
        scraper.SetLang.assert_called_once()
        scraper.CloseWebDriver.assert_called_once()
