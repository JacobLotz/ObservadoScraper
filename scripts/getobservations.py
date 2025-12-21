# Import classes
from classes import ObservationCollectionScraper, ObservationProcessor

"""
This script demonstrates the new modular architecture:
1. Scrape data using ObservationCollectionScraper
2. Save scraped data to CSV files
3. Load data and process using ObservationProcessor
4. Export to KML files
"""


# Example 1: Kleine Strandloper
print("\nProcessing Kleine Strandloper...")
link = "https://waarneming.nl/species/133/observations/?date_after=2025-07-25&date_before=2025-08-07&country_division=2&advanced=on&page=2"
scraper = ObservationCollectionScraper(link)
df = scraper.scrape()
scraper.save(df, "kleine-strandloper_data.csv")

processor = ObservationProcessor(df)
processor.to_kml("kleine-strandloper.kml")

print("\nAll observations processed successfully!")
