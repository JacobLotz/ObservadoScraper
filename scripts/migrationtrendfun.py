import calendar
import datetime
import logging

from classes import MigrationProcessor, MigrationScraper

logger = logging.getLogger(__name__)


def get_month_end(date_in_):
    return calendar.monthrange(date_in_.year, date_in_.month)[1]


def get_start_dates(month_start_, month_end_, year_):
    start_dates = []
    month = month_start_

    while month != month_end_ + 1:
        date = datetime.date(year_, month, 1)
        start_dates.append(datetime.date(year_, month, 1))
        start_dates.append(datetime.date(year_, month, 11))
        start_dates.append(datetime.date(year_, month, 21))
        month += 1

    return start_dates


def get_end_dates(month_start_, month_end_, year_):
    end_dates = []
    month = month_start_

    while month != month_end_ + 1:
        date = datetime.date(year_, month, 1)
        end = get_month_end(date)
        end_dates.append(datetime.date(year_, month, 11))
        end_dates.append(datetime.date(year_, month, 21))
        end_dates.append(datetime.date(year_, month, end))
        month += 1

    return end_dates


def get_species_plot(year_start, year_end, month_start, month_end, species_id, name):
    """
    Scrape migration trend data and create plot for a species.

    Demonstrates the new modular architecture:
    1. Generate date ranges
    2. Scrape data using MigrationScraper
    3. Save scraped data to CSV
    4. Load and process using MigrationProcessor
    5. Generate plot

    Args:
        year_start: First year to include
        year_end: Last year to include
        month_start: Start month (1-12)
        month_end: End month (1-12)
        species_id: Species ID for waarneming.nl
        name: Species name for plot title
    """
    logger.info(f"Working on: {name}")

    # Generate date bins
    years_range = range(year_start, year_end + 1, 1)
    date_ranges = []

    for year in years_range:
        bins_start = get_start_dates(month_start, month_end, year)
        bins_end = get_end_dates(month_start, month_end, year)

        for start, end in zip(bins_start, bins_end):
            date_ranges.append((start, end))

    # Scrape data
    scraper = MigrationScraper("https://waarneming.nl")
    df = scraper.scrape_date_ranges(species_id, date_ranges)

    # Save scraped data
    csv_filename = f"{species_id}_{name.replace(' ', '_')}_data.csv"
    scraper.save(df, csv_filename)

    # Process and plot
    processor = MigrationProcessor(df)
    plot_file = processor.plot_species_trend(name, month_start, month_end)

    logger.info(f"Completed: {name}")
    return plot_file
