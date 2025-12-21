from .base import ScrapeBase

# Scraper class for extracting data from a single observation page
class ObservationScraper(ScrapeBase):
    """
    Scrapes data from a single waarneming.nl observation page.
    Returns observation data as a dictionary.
    """

    def __init__(self, Link, browser):
        self.browser = browser
        self.Link = Link
        self.SetParam()

    def scrape(self):
        """
        Scrapes the observation page and returns data as a dictionary.
        Returns None if GPS data is obscured or scraping fails.
        """
        self.GetSoup()

        try:
            name = self.PageSoup.find_all("span", {"class": "species-common-name"})[0].text.strip()
        except (IndexError, AttributeError):
            return None

        # Extract observation details table
        try:
            infotable = self.PageSoup.find_all("table", {"class": "table table-condensed", "id": "observation_details"})
            info = infotable[0].find_all("td")
            datetime_str = info[0].text.strip()
            location_name = info[4].text.strip()
        except (IndexError, AttributeError):
            return None

        # Parse date/time
        datetime_list = datetime_str.replace('-', ' ').split(' ')
        year = datetime_list[0]
        month = datetime_list[1]
        day = datetime_list[2]
        month_day = f"{datetime_list[2]}-{datetime_list[1]}"
        time = datetime_list[3] if len(datetime_list) == 4 else '-'

        # Get GPS coordinates - skip if obscured
        location = self.PageSoup.find_all("span", {"class": "teramap-coordinates-coords"})
        if not location:
            return None

        location = location[0].text.strip().split(", ")
        latitude = location[0]
        longitude = location[1]

        # Find description
        description_elem = self.PageSoup.find("div", {"class": "goog-trans-section"})
        description = description_elem.get_text() if description_elem else ""

        return {
            'name': name,
            'datetime': datetime_str,
            'year': year,
            'month': month,
            'day': day,
            'month_day': month_day,
            'time': time,
            'location_name': location_name,
            'latitude': latitude,
            'longitude': longitude,
            'description': description,
            'url': self.Link
        }
