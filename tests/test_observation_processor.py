import pandas as pd
import os
import tempfile
import json
from classes import ObservationProcessor, ObservationCollectionScraper


class TestObservationProcessor:
    """Tests for ObservationProcessor using mocked CSV data"""

    def setup_method(self, method):
        print(f"Setting up {method}")

        # Load mock data
        test_dir = os.path.dirname(__file__)
        mock_file = os.path.join(test_dir, 'mocks', 'observations_mock.csv')
        self.df = pd.read_csv(mock_file)
        self.processor = ObservationProcessor(self.df)

    def test_initialization(self):
        """Test that processor initializes with DataFrame"""
        assert len(self.processor.get_dataframe()) == 5
        assert 'name' in self.processor.get_dataframe().columns

    def test_filter_selffinds(self):
        """Test filtering for self-finds"""
        filtered = self.processor.filter_selffinds()
        df_result = filtered.get_dataframe()

        # Should find 3 self-finds (Self, qwerty, Self)
        assert len(df_result) == 3

        # Check that correct observations are included
        names = df_result['name'].tolist()
        assert 'Boswitje' in names  # "Self found"
        assert 'Staartblauwtje' in names  # "qwerty"
        assert 'Sleedoornpage' in names  # "Self observed"

        # Check that non-selffind is excluded
        assert 'Kaasjeskruiddikkopje' not in names

    def test_assign_points(self):
        """Test assigning points to observations"""
        # Create temporary points file
        points_dict = {
            'Boswitje': 10,
            'Kleine Weerschijnvlinder': 5,
            'Staartblauwtje': 15,
            'Kaasjeskruiddikkopje': 8,
            'Sleedoornpage': 12
        }

        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(points_dict, f)
            temp_points_file = f.name

        try:
            self.processor.assign_points(points_file=temp_points_file)
            df = self.processor.get_dataframe()

            assert 'points' in df.columns
            assert df[df['name'] == 'Boswitje']['points'].iloc[0] == 10
            assert df[df['name'] == 'Staartblauwtje']['points'].iloc[0] == 15
        finally:
            os.unlink(temp_points_file)

    def test_calculate_total_points(self):
        """Test calculating total points"""
        points_dict = {
            'Boswitje': 10,
            'Kleine Weerschijnvlinder': 5,
            'Staartblauwtje': 15,
            'Kaasjeskruiddikkopje': 8,
            'Sleedoornpage': 12
        }

        self.processor.assign_points(points_dict=points_dict)
        total = self.processor.calculate_total_points()

        # 10 + 5 + 15 + 8 + 12 = 50
        assert total == 50

    def test_filter_by_species(self):
        """Test filtering by species names"""
        species_to_keep = ['Boswitje', 'Staartblauwtje']
        filtered = self.processor.filter_by_species(species_to_keep)
        df_result = filtered.get_dataframe()

        assert len(df_result) == 2
        assert set(df_result['name'].tolist()) == set(species_to_keep)

    def test_sort_by_date(self):
        """Test sorting by date"""
        self.processor.sort_by_date(ascending=True)
        df = self.processor.get_dataframe()

        # Check that dates are in ascending order
        dates = df['datetime'].tolist()
        assert dates == sorted(dates)

    def test_to_kml(self):
        """Test KML export"""
        with tempfile.NamedTemporaryFile(suffix='.kml', delete=False) as f:
            temp_kml = f.name

        try:
            self.processor.to_kml(temp_kml)
            assert os.path.exists(temp_kml)
            assert os.path.getsize(temp_kml) > 0
        finally:
            if os.path.exists(temp_kml):
                os.unlink(temp_kml)

    def test_to_text_report(self):
        """Test text report generation"""
        points_dict = {'Boswitje': 10, 'Kleine Weerschijnvlinder': 5}
        self.processor.assign_points(points_dict=points_dict)

        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
            temp_report = f.name

        try:
            self.processor.to_text_report(temp_report, title="Test Report")
            assert os.path.exists(temp_report)

            with open(temp_report, 'r') as f:
                content = f.read()
                assert 'Test Report' in content
                assert 'Boswitje' in content
        finally:
            if os.path.exists(temp_report):
                os.unlink(temp_report)

    def test_get_summary(self):
        """Test summary statistics"""
        summary = self.processor.get_summary()

        assert summary['total_observations'] == 5
        assert summary['unique_species'] == 5
        assert 'Boswitje' in summary['species_list']

    def test_get_summary_with_points(self):
        """Test summary with points assigned"""
        points_dict = {'Boswitje': 10, 'Kleine Weerschijnvlinder': 5}
        self.processor.assign_points(points_dict=points_dict)

        summary = self.processor.get_summary()
        assert 'total_points' in summary

    def test_chained_operations(self):
        """Test chaining multiple operations"""
        points_dict = {
            'Boswitje': 10,
            'Staartblauwtje': 15,
            'Sleedoornpage': 12
        }

        # Chain: filter selffinds -> assign points -> sort
        result = (self.processor
                  .filter_selffinds()
                  .assign_points(points_dict=points_dict)
                  .sort_by_date(ascending=True))

        df = result.get_dataframe()

        # Should have 3 selffind observations
        assert len(df) == 3

        # Should have points assigned
        assert 'points' in df.columns

        # Should be sorted
        dates = df['datetime'].tolist()
        assert dates == sorted(dates)

    def test_load_save_csv(self):
        """Test saving and loading CSV"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            temp_csv = f.name

        try:
            # Save
            scraper = ObservationCollectionScraper("dummy_link")
            scraper.save(self.df, temp_csv)

            # Load
            loaded_df = ObservationCollectionScraper.load(temp_csv)

            assert len(loaded_df) == len(self.df)
            assert list(loaded_df.columns) == list(self.df.columns)
        finally:
            if os.path.exists(temp_csv):
                os.unlink(temp_csv)
