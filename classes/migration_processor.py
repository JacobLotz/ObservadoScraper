import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import MultipleLocator

from .utils import get_results_path


class MigrationProcessor:
    """
    Processes migration trend data from pandas DataFrame.
    Handles plotting and analysis of migration patterns.
    """

    def __init__(self, df):
        """
        Initialize processor with migration DataFrame.

        Args:
            df: pandas DataFrame with columns: start_date, end_date, n_squares, species_id
        """
        self.df = df.copy()

    def _divide_chunks(self, lst, n):
        """Divide list into chunks of size n"""
        for i in range(0, len(lst), n):
            yield lst[i : i + n]

    def plot_species_trend(self, species_name, month_start=1, month_end=12, output_file=None):
        """
        Create a migration trend plot for a species.

        Args:
            species_name: Name of the species for plot title
            month_start: Start month (1-12)
            month_end: End month (1-12)
            output_file: Path to save plot (if None, uses species_id-species_name.png)

        Returns:
            Path to saved plot file
        """
        if len(self.df) == 0:
            print(f"No data available for {species_name}")
            return None

        # Extract years from dates
        self.df["year"] = pd.to_datetime(self.df["start_date"]).dt.year
        years = sorted(self.df["year"].unique())
        n_years = len(years)

        # Create x-axis labels (3 periods per month)
        x_axis = [
            "Jan",
            " ",
            " ",
            "Feb",
            " ",
            " ",
            "Maa",
            " ",
            " ",
            "Apr",
            " ",
            " ",
            "Mei",
            " ",
            " ",
            "Jun",
            " ",
            " ",
            "Jul",
            " ",
            " ",
            "Aug",
            " ",
            " ",
            "Sep",
            " ",
            " ",
            "Okt",
            " ",
            " ",
            "Nov",
            " ",
            " ",
            "Dec",
            " ",
            " ",
        ]

        # Filter to requested months
        x_axis = x_axis[(month_start - 1) * 3 : (month_end * 3)]
        X_axis = np.arange(len(x_axis))

        # Get n_squares data and divide by year
        y = self.df["n_squares"].tolist()
        yy = list(self._divide_chunks(y, len(x_axis)))

        # Compute mean (excluding last year from average)
        if len(yy) > 1:
            yy_premean = yy[0:-1]
            yy_mean = np.mean(np.array(yy_premean), axis=0).tolist()
        else:
            yy_mean = yy[0] if len(yy) > 0 else []

        # Set up plot
        major_locator = MultipleLocator(3)
        minor_locator = MultipleLocator(1)

        plt.figure(figsize=(8, 3))

        # Plot each year
        for yyy, year in zip(yy, years):
            plt.plot(X_axis + 0.5, yyy, label=str(year), alpha=0.5, linestyle="dashed")

        # Plot mean
        if len(yy_mean) > 0:
            plt.plot(X_axis + 0.5, yy_mean, color="black", label="gem.")

        # Configure axes
        plt.gca().set_ylim(bottom=0)
        plt.gca().set_xlim(left=0, right=len(x_axis))
        plt.xticks(X_axis, x_axis)
        plt.gca().xaxis.set_major_locator(major_locator)
        plt.gca().xaxis.set_minor_locator(minor_locator)

        plt.title(species_name)
        plt.legend()

        # Save plot
        if output_file is None:
            species_id = (
                self.df["species_id"].iloc[0] if "species_id" in self.df.columns else "unknown"
            )
            output_file = f"{species_id}-{species_name.replace(' ', '_')}.png"

        filepath = get_results_path(output_file)
        plt.savefig(filepath)
        plt.close()

        print(f"Saved plot to: {filepath}")
        return filepath

    def get_dataframe(self):
        """
        Get the underlying DataFrame.

        Returns:
            pandas DataFrame
        """
        return self.df

    def get_summary(self):
        """
        Get summary statistics of the migration data.

        Returns:
            Dictionary with summary information
        """
        summary = {
            "total_data_points": len(self.df),
            "date_range": {"start": self.df["start_date"].min(), "end": self.df["end_date"].max()},
            "max_squares": int(self.df["n_squares"].max()),
            "mean_squares": float(self.df["n_squares"].mean()),
        }

        return summary
