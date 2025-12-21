# Import classes
import logging
import os
from datetime import date

from classes import ObservationCollectionScraper, ObservationProcessor
from classes.utils import get_results_path

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

"""
This script updates the self-found competition by checking the observations of the
participating members for markers "self" or "qwerty". If the claim should be awarded
with points in the competition it will assign the points and print the details. All
the observations are printed to a file.

Demonstrates the new modular architecture:
1. Scrape observations for each participant
2. Save scraped data to CSV files
3. Load and process (filter self-finds, assign points)
4. Generate ranking report
"""

start = "2024-01-01"
end = date.today()

# Get results file path (in results/ directory)
filename = get_results_path("results.txt")

# Load points mapping (from data/ directory, not results/)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
points_file = os.path.join(parent_dir, "data/points.json")

# Initialize results file
with open(filename, "w+") as f:
    f.write(
        "{:<27}{:<6}{:<1}{:<10}{:<24}{:<20}\n".format(
            "Soort", "Punten", " ", "Datum", "Locatie", "Laatste update: " + str(end)
        )
    )
    f.write(
        "----------------------------------------------------------------------------------------------"
    )

# Participant configuration
participants = [
    {"name": "Daan", "user_id": "22414"},
    {"name": "Ruben", "user_id": "3219"},
    {"name": "Jurriën", "user_id": "17815"},
    {"name": "Jacob", "user_id": "41541"},
]

# Process each participant
for participant in participants:
    logger.info(f"\n{'='*50}")
    logger.info(f"Processing {participant['name']}...")
    logger.info(f"{'='*50}")

    # Build link
    link = (
        f"https://waarneming.nl/users/{participant['user_id']}/observations/"
        f"?date_after={start}&date_before={end}&species_group=1&rarity=2&page=1"
    )

    # Import points to filter species during scraping
    import json

    with open(points_file, "r") as f:
        points_dict = json.load(f)
    species_filter = set(points_dict.keys())

    # Scrape observations
    scraper = ObservationCollectionScraper(link)
    df = scraper.scrape(species_filter=species_filter)

    # Save scraped data
    csv_filename = f"{participant['name'].lower()}_observations.csv"
    scraper.save(df, csv_filename)

    # Process observations
    processor = ObservationProcessor(df)

    # Filter for self-finds
    processor = processor.filter_selffinds()

    # Filter by species that have points
    processor = processor.filter_by_species(list(species_filter))

    # Assign points
    processor.assign_points(points_file=points_file)

    # Sort by date (oldest first)
    processor.sort_by_date(ascending=True)

    # Generate report section (filename is just the name, not full path)
    processor.to_text_report(
        "results.txt",
        title=f'\n\n----------------------------------------------------------------------------------------------\n{participant["name"]}',
    )

    # Print summary
    summary = processor.get_summary()
    logger.info(f"\nSummary for {participant['name']}:")
    logger.info(f"  Self-finds: {summary['total_observations']}")
    logger.info(f"  Total points: {summary.get('total_points', 0)}")

logger.info("\n" + "=" * 50)
logger.info("Ranking update complete!")
logger.info(f"Report saved to: {filename}")
logger.info("=" * 50)
