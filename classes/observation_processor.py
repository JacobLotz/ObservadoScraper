import json
import os

import pandas as pd
import simplekml

from .utils import get_results_path


class ObservationProcessor:
    """
    Processes observation data from pandas DataFrame.
    Handles KML export, self-find detection, and ranking calculations.
    """

    def __init__(self, df):
        """
        Initialize processor with observation DataFrame.

        Args:
            df: pandas DataFrame with observation data
        """
        self.df = df.copy()

    def filter_selffinds(self):
        """
        Filter observations to only include self-finds.
        Self-finds are identified by keywords in the description.

        Returns:
            New ObservationProcessor with filtered data
        """
        selffind_keywords = ["Self", "self", "qwerty", "Qwerty"]

        def is_selffind(description):
            """
            Check if an observation description contains self-find keywords.

            Args:
                description: Observation description text (may be NaN or empty)

            Returns:
                True if description contains any self-find keyword, False otherwise
            """
            if pd.isna(description) or description == "":
                return False
            return any(keyword in str(description) for keyword in selffind_keywords)

        filtered_df = self.df[self.df["description"].apply(is_selffind)].copy()
        return ObservationProcessor(filtered_df)

    def assign_points(self, points_dict=None, points_file=None):
        """
        Assign point values to observations based on species.

        Args:
            points_dict: Dictionary mapping species names to point values
            points_file: Path to JSON file with points mapping (default: data/points.json)

        Returns:
            self (for method chaining)
        """
        if points_dict is None:
            if points_file is None:
                # Default to data/points.json
                parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
                points_file = os.path.join(parent_dir, "data/points.json")

            with open(points_file, "r") as f:
                points_dict = json.load(f)

        # Assign points based on species name
        self.df["points"] = self.df["name"].map(points_dict).fillna(0).astype(int)

        return self

    def calculate_total_points(self):
        """
        Calculate total points.

        Returns:
            Total points as integer
        """
        if "points" not in self.df.columns:
            raise ValueError("Points not assigned. Call assign_points() first.")

        return int(self.df["points"].sum())

    def filter_by_species(self, species_list):
        """
        Filter observations by species names.

        Args:
            species_list: List of species names to keep

        Returns:
            New ObservationProcessor with filtered data
        """
        filtered_df = self.df[self.df["name"].isin(species_list)].copy()
        return ObservationProcessor(filtered_df)

    def sort_by_date(self, ascending=False):
        """
        Sort observations by date.

        Args:
            ascending: If True, sort oldest first. If False (default), sort newest first.

        Returns:
            self (for method chaining)
        """
        self.df = self.df.sort_values("datetime", ascending=ascending)
        return self

    def to_kml(self, filename):
        """
        Export observations to KML file in the results directory.

        Args:
            filename: Filename (not full path) for output KML file, e.g., 'output.kml'
        """
        kml = simplekml.Kml()

        for _, row in self.df.iterrows():
            kml.newpoint(
                name=row["name"],
                coords=[(row["longitude"], row["latitude"])],
                description=f"Date: {row['datetime']}",
            )

        filepath = get_results_path(filename)
        kml.save(filepath, format=True)
        print(f"Saved KML to: {filepath}")

    def to_text_report(self, filename, title="Observations"):
        """
        Export observations to formatted text file (for ranking reports) in the results directory.

        Args:
            filename: Filename (not full path) for output text file, e.g., 'report.txt'
            title: Title for the report section
        """
        filepath = get_results_path(filename)
        with open(filepath, "a") as f:
            f.write(f"\n{title}\n")

            for _, row in self.df.iterrows():
                points_str = f"{row['points']:>6}" if "points" in self.df.columns else "     -"
                line = "{:<27}{}{:<1}{:<10}{:<60}\n".format(
                    row["name"], points_str, " ", row["month_day"], row["location_name"]
                )
                f.write(line)

            if "points" in self.df.columns:
                total = self.calculate_total_points()
                f.write("\n")
                f.write("{:<27}{:>6}\n".format("Totaal: ", total))

        print(f"Appended report to: {filepath}")

    def get_dataframe(self):
        """
        Get the underlying DataFrame.

        Returns:
            pandas DataFrame
        """
        return self.df

    def get_summary(self):
        """
        Get summary statistics of the observations.

        Returns:
            Dictionary with summary information
        """
        summary = {
            "total_observations": len(self.df),
            "unique_species": self.df["name"].nunique(),
            "species_list": sorted(self.df["name"].unique().tolist()),
        }

        if "points" in self.df.columns:
            summary["total_points"] = self.calculate_total_points()

        return summary
