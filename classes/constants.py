"""
Constants for the ObservadoScraper project.

This module defines all magic numbers and configuration constants used throughout the codebase.
"""

# Default scraper settings
DEFAULT_WAIT_TIME = 0  # Default wait time in seconds before parsing page
DEFAULT_LANGUAGE = "nl"  # Default language code for waarneming.nl

# WebDriver timeouts (in seconds)
LANGUAGE_BUTTON_TIMEOUT = 10  # Timeout for language selection button to become clickable
MAP_LOADING_TIMEOUT = 4  # Timeout for map tiles and grid data to load
LEGEND_PANEL_TIMEOUT = 2  # Timeout for map legend panel to appear

# Migration scraper thresholds
MIN_GRID_CELLS_RENDERED = (
    10  # Minimum number of grid cells to wait for before considering map loaded
)
