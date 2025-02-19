import os


def get_data_dir():
    """
    Returns the path to the data directory, which is assumed to be located at <project_root>/data.
    """
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data')) 