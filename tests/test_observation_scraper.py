import os
from unittest.mock import Mock
from bs4 import BeautifulSoup
from classes import ObservationScraper


class TestObservationScraper:
    """Tests for ObservationScraper using mocked HTML"""

    def setup_method(self, method):
        print(f"Setting up {method}")
        self.test_dir = os.path.dirname(__file__)

    def _load_mock_html(self, filename):
        """Load mock HTML file and return BeautifulSoup object"""
        mock_file = os.path.join(self.test_dir, 'mocks', filename)
        with open(mock_file, 'r', encoding='utf-8') as f:
            html = f.read()
        return BeautifulSoup(html, 'html.parser')

    def test_scrape_normal_observation(self):
        """Test scraping a normal observation with GPS coordinates"""
        # Create mock browser
        mock_browser = Mock()

        # Create scraper instance
        scraper = ObservationScraper("https://waarneming.nl/observation/382543115/", mock_browser)

        # Mock the GetSoup method to use our HTML mock
        mock_soup = self._load_mock_html('observation_page.html')
        scraper.PageSoup = mock_soup

        # Scrape without calling GetSoup (which would use Selenium)
        scraper.GetSoup = Mock()  # Mock out GetSoup
        result = scraper.scrape()

        # Verify results
        assert result is not None
        assert result['name'] == 'Gewone Zeehond'
        assert result['year'] == '2025'
        assert result['month'] == '12'
        assert result['day'] == '14'
        assert result['time'] == '-'
        assert result['month_day'] == '14-12'
        assert result['datetime'] == '2025-12-14'
        assert result['location_name'] == 'Ter Heijde - Zandmotor (ZH)'
        assert result['latitude'] == '52.05759'
        assert result['longitude'] == '4.19180'
        assert 'Self found' in result['description']
        assert result['url'] == 'https://waarneming.nl/observation/382543115/'

    def test_scrape_selffind_observation_257848200(self):
        """Test scraping observation 257848200 - Vale Gierzwaluw with self-find marker"""
        mock_browser = Mock()
        scraper = ObservationScraper("https://waarneming.nl/observation/257848200/", mock_browser)

        # Mock the GetSoup method to use our HTML mock
        mock_soup = self._load_mock_html('observation_257848200.html')
        scraper.PageSoup = mock_soup
        scraper.GetSoup = Mock()

        result = scraper.scrape()

        # Verify results
        assert result is not None
        assert result['name'] == 'Vale Gierzwaluw'
        assert result['year'] == '2022'
        assert result['month'] == '10'
        assert result['day'] == '23'
        assert result['time'] == '-'
        assert result['month_day'] == '23-10'
        assert result['datetime'] == '2022-10-23'
        assert result['location_name'] == 'Maasvlakte 2 (ZH)'
        assert result['latitude'] == '51.95211'
        assert result['longitude'] == '3.96657'
        assert 'self' in result['description']
        assert result['url'] == 'https://waarneming.nl/observation/257848200/'

    def test_scrape_obscured_observation(self):
        """Test scraping an observation with obscured GPS coordinates"""
        mock_browser = Mock()
        scraper = ObservationScraper("https://waarneming.nl/observation/999999/", mock_browser)

        # Mock the GetSoup method
        mock_soup = self._load_mock_html('observation_page_obscured.html')
        scraper.PageSoup = mock_soup
        scraper.GetSoup = Mock()

        result = scraper.scrape()

        # Should return None when GPS is obscured
        assert result is None

    def test_scrape_observation_without_time(self):
        """Test scraping observation with only date (no time)"""
        mock_browser = Mock()
        scraper = ObservationScraper("https://waarneming.nl/observation/123456/", mock_browser)

        # Create modified HTML without time
        html = """
        <html>
            <div class="observation-header">
                <h1><span class="species-common-name">Test Species</span></h1>
            </div>
            <table class="table table-condensed" id="observation_details">
                <tbody>
                    <tr><th>Datum</th><td>2025-06-15</td></tr>
                    <tr><th>Aantal</th><td>1</td></tr>
                    <tr><th>Levensstadium</th><td>Adult</td></tr>
                    <tr><th>Activiteit</th><td>Vliegend</td></tr>
                    <tr><th>Locatie</th><td>Test Location</td></tr>
                </tbody>
            </table>
            <div class="map-section">
                <div class="teramap-coordinates">
                    <span class="teramap-coordinates-coords">52.1234, 4.5678</span>
                </div>
            </div>
        </html>
        """

        scraper.PageSoup = BeautifulSoup(html, 'html.parser')
        scraper.GetSoup = Mock()

        result = scraper.scrape()

        assert result is not None
        assert result['time'] == '-'
        assert result['datetime'] == '2025-06-15'

    def test_scrape_with_empty_description(self):
        """Test scraping observation without description"""
        mock_browser = Mock()
        scraper = ObservationScraper("https://waarneming.nl/observation/123456/", mock_browser)

        html = """
        <html>
            <div class="observation-header">
                <h1><span class="species-common-name">Test Species</span></h1>
            </div>
            <table class="table table-condensed" id="observation_details">
                <tbody>
                    <tr><th>Datum</th><td>2025-06-15 10:00</td></tr>
                    <tr><th>Aantal</th><td>1</td></tr>
                    <tr><th>Levensstadium</th><td>Adult</td></tr>
                    <tr><th>Activiteit</th><td>Vliegend</td></tr>
                    <tr><th>Locatie</th><td>Test Location</td></tr>
                </tbody>
            </table>
            <div class="map-section">
                <div class="teramap-coordinates">
                    <span class="teramap-coordinates-coords">52.1234, 4.5678</span>
                </div>
            </div>
        </html>
        """

        scraper.PageSoup = BeautifulSoup(html, 'html.parser')
        scraper.GetSoup = Mock()

        result = scraper.scrape()

        assert result is not None
        assert result['description'] == ''

    def test_scrape_malformed_page(self):
        """Test scraping a page with missing required elements"""
        mock_browser = Mock()
        scraper = ObservationScraper("https://waarneming.nl/observation/123456/", mock_browser)

        # HTML missing species name
        html = """
        <html>
            <div class="observation-header">
                <h1></h1>
            </div>
        </html>
        """

        scraper.PageSoup = BeautifulSoup(html, 'html.parser')
        scraper.GetSoup = Mock()

        result = scraper.scrape()

        # Should return None when required elements are missing
        assert result is None

    def test_date_parsing_variations(self):
        """Test that different date formats are parsed correctly"""
        mock_browser = Mock()
        scraper = ObservationScraper("https://waarneming.nl/observation/123456/", mock_browser)

        # Test with different date/time formats
        test_cases = [
            ("2025-12-14 13:54", "2025", "12", "14", "13:54", "14-12"),
            ("2025-01-05 09:00", "2025", "01", "05", "09:00", "05-01"),
            ("2024-11-30", "2024", "11", "30", "-", "30-11"),
        ]

        for datetime_str, exp_year, exp_month, exp_day, exp_time, exp_month_day in test_cases:
            html = f"""
            <html>
                <div class="observation-header">
                    <h1><span class="species-common-name">Test Species</span></h1>
                </div>
                <table class="table table-condensed" id="observation_details">
                    <tbody>
                        <tr><th>Datum</th><td>{datetime_str}</td></tr>
                        <tr><th>Aantal</th><td>1</td></tr>
                        <tr><th>Levensstadium</th><td>Adult</td></tr>
                        <tr><th>Activiteit</th><td>Vliegend</td></tr>
                        <tr><th>Locatie</th><td>Test Location</td></tr>
                    </tbody>
                </table>
                <div class="map-section">
                    <div class="teramap-coordinates">
                        <span class="teramap-coordinates-coords">52.1234, 4.5678</span>
                    </div>
                </div>
            </html>
            """

            scraper.PageSoup = BeautifulSoup(html, 'html.parser')
            scraper.GetSoup = Mock()

            result = scraper.scrape()

            assert result is not None, f"Failed for datetime: {datetime_str}"
            assert result['year'] == exp_year
            assert result['month'] == exp_month
            assert result['day'] == exp_day
            assert result['time'] == exp_time
            assert result['month_day'] == exp_month_day
