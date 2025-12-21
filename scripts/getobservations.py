# Import classes
from classes import ObservationCollectionScraper, ObservationProcessor

"""
This script demonstrates the new modular architecture:
1. Scrape data using ObservationCollectionScraper
2. Save scraped data to CSV files
3. Load data and process using ObservationProcessor
4. Export to KML files
"""

# Example 1: Kemphaan
#print("Processing Kemphaan...")
#link = "https://waarneming.nl/species/24/observations/?date_after=2025-07-25&date_before=2025-08-07&country_division=2&advanced=on&page=2"
#scraper = ObservationCollectionScraper(link)
#df = scraper.scrape()
#scraper.save(df, "kemphaan_data.csv")
#
## Process the data
#processor = ObservationProcessor(df)
#processor.to_kml("kemphaan.kml")


# Example 2: Kleine Strandloper
print("\nProcessing Kleine Strandloper...")
link = "https://waarneming.nl/species/133/observations/?date_after=2025-07-25&date_before=2025-08-07&country_division=2&advanced=on&page=2"
scraper = ObservationCollectionScraper(link)
df = scraper.scrape()
scraper.save(df, "kleine-strandloper_data.csv")

processor = ObservationProcessor(df)
processor.to_kml("kleine-strandloper.kml")


# Example 3: Bonte Strandloper
#print("\nProcessing Bonte Strandloper...")
#link = "https://waarneming.nl/species/68/observations/?date_after=2025-07-25&date_before=2025-08-07&country_division=2&advanced=on&page=2"
#scraper = ObservationCollectionScraper(link)
#df = scraper.scrape()
#scraper.save(df, "bonte-strandloper_data.csv")
#
#processor = ObservationProcessor(df)
#processor.to_kml("bonte-strandloper.kml")
#
#
## Example 4: Groenpootruiter
#print("\nProcessing Groenpootruiter...")
#link = "https://waarneming.nl/species/108/observations/?date_after=2025-07-25&date_before=2025-08-07&country_division=2&advanced=on&page=2"
#scraper = ObservationCollectionScraper(link)
#df = scraper.scrape()
#scraper.save(df, "groenpootruiter_data.csv")
#
#processor = ObservationProcessor(df)
#processor.to_kml("groenpootruiter.kml")
#
#
## Example 5: Krombekstrandloper
#print("\nProcessing Krombekstrandloper...")
#link = "https://waarneming.nl/species/283/observations/?date_after=2025-07-25&date_before=2025-08-07&country_division=2&advanced=on&page=2"
#scraper = ObservationCollectionScraper(link)
#df = scraper.scrape()
#scraper.save(df, "krombekstrandloper_data.csv")
#
#processor = ObservationProcessor(df)
#processor.to_kml("krombekstrandloper.kml")
#
#
## Example 6: Kanoet
#print("\nProcessing Kanoet...")
#link = "https://waarneming.nl/species/125/observations/?date_after=2025-07-25&date_before=2025-08-07&country_division=2&advanced=on&page=2"
#scraper = ObservationCollectionScraper(link)
#df = scraper.scrape()
#scraper.save(df, "kanoet_data.csv")
#
#processor = ObservationProcessor(df)
#processor.to_kml("kanoet.kml")
#
#
## Example 7: Lachstern
#print("\nProcessing Lachstern...")
#link = "https://waarneming.nl/species/368/observations/?date_after=2025-07-25&date_before=2025-08-07&country_division=2&advanced=on&page=2"
#scraper = ObservationCollectionScraper(link)
#df = scraper.scrape()
#scraper.save(df, "lachstern_data.csv")
#
#processor = ObservationProcessor(df)
#processor.to_kml("lachstern.kml")

print("\nAll observations processed successfully!")
