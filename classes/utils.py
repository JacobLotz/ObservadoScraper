import os


def ensure_results_dir():
    """
    Ensure the results directory exists. Creates it if it doesn't exist.

    Returns:
        str: Path to the results directory
    """
    # Get the project root directory (parent of classes/)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    results_dir = os.path.join(project_root, "results")

    # Create directory if it doesn't exist
    if not os.path.exists(results_dir):
        os.makedirs(results_dir)
        print(f"Created results directory: {results_dir}")

    return results_dir


def get_results_path(filename):
    """
    Get the full path for a file in the results directory.

    Args:
        filename: Name of the file (e.g., 'output.csv', 'data.kml')

    Returns:
        str: Full path to the file in the results directory
    """
    results_dir = ensure_results_dir()
    return os.path.join(results_dir, filename)
