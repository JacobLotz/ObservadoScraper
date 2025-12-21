import pandas as pd
import os
import tempfile
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for testing
import matplotlib.pyplot as plt
from classes import MigrationProcessor, MigrationScraper


class TestMigrationProcessor:
    """Tests for MigrationProcessor using mocked CSV data"""

    def setup_method(self, method):
        print(f"Setting up {method}")

        # Load mock data
        test_dir = os.path.dirname(__file__)
        mock_file = os.path.join(test_dir, 'mocks', 'migration_mock.csv')
        self.df = pd.read_csv(mock_file)

        # Convert date columns to datetime
        self.df['start_date'] = pd.to_datetime(self.df['start_date'])
        self.df['end_date'] = pd.to_datetime(self.df['end_date'])

        self.processor = MigrationProcessor(self.df)

    def teardown_method(self, method):
        print(f"Tearing down {method}")
        # Clean up any remaining matplotlib figures
        plt.close('all')

    def test_initialization(self):
        """Test that processor initializes with DataFrame"""
        assert len(self.processor.get_dataframe()) == 12
        assert 'n_squares' in self.processor.get_dataframe().columns

    def test_plot_species_trend(self):
        """Test creating a species trend plot"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            temp_plot = f.name

        try:
            output_file = self.processor.plot_species_trend(
                species_name="Test Species",
                month_start=1,
                month_end=2,
                output_file=temp_plot
            )

            assert os.path.exists(temp_plot)
            assert os.path.getsize(temp_plot) > 0
            assert output_file == temp_plot
        finally:
            if os.path.exists(temp_plot):
                os.unlink(temp_plot)
            plt.close('all')

    def test_plot_with_auto_filename(self):
        """Test plot generation with automatic filename"""
        output_file = self.processor.plot_species_trend(
            species_name="Breedbekstrandloper",
            month_start=1,
            month_end=2
        )

        try:
            assert os.path.exists(output_file)
            assert 'Breedbekstrandloper' in output_file
        finally:
            if os.path.exists(output_file):
                os.unlink(output_file)
            plt.close('all')

    def test_get_summary(self):
        """Test summary statistics"""
        summary = self.processor.get_summary()

        assert summary['total_data_points'] == 12
        assert 'date_range' in summary
        assert summary['max_squares'] == 60
        assert summary['mean_squares'] > 0

    def test_get_dataframe(self):
        """Test getting the underlying DataFrame"""
        df = self.processor.get_dataframe()

        assert isinstance(df, pd.DataFrame)
        assert len(df) == 12
        assert 'species_id' in df.columns

    def test_load_save_csv(self):
        """Test saving and loading migration CSV"""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            temp_csv = f.name

        try:
            # Save
            scraper = MigrationScraper("dummy_link")
            scraper.save(self.df, temp_csv)

            # Load
            loaded_df = MigrationScraper.load(temp_csv)

            assert len(loaded_df) == len(self.df)
            assert list(loaded_df.columns) == list(self.df.columns)

            # Check that dates were properly converted
            assert pd.api.types.is_datetime64_any_dtype(loaded_df['start_date'])
            assert pd.api.types.is_datetime64_any_dtype(loaded_df['end_date'])
        finally:
            if os.path.exists(temp_csv):
                os.unlink(temp_csv)

    def test_empty_dataframe(self):
        """Test processor behavior with empty DataFrame"""
        empty_df = pd.DataFrame(columns=['start_date', 'end_date', 'n_squares', 'species_id'])
        processor = MigrationProcessor(empty_df)

        result = processor.plot_species_trend("Empty Species", 1, 12)
        assert result is None

    def test_plot_different_month_ranges(self):
        """Test plotting with different month ranges"""
        with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as f:
            temp_plot = f.name

        try:
            # Test with just January
            output_file = self.processor.plot_species_trend(
                species_name="Test Species",
                month_start=1,
                month_end=1,
                output_file=temp_plot
            )

            assert os.path.exists(temp_plot)
        finally:
            if os.path.exists(temp_plot):
                os.unlink(temp_plot)
            plt.close('all')
