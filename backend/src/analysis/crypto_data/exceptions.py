class DataLoaderError(Exception):
    """Base class for exceptions in this module."""
    pass

class DatabaseConnectionError(DataLoaderError):
    """Exception raised for errors in the database connection."""
    pass

class DataInsertionError(DataLoaderError):
    """Exception raised for errors during data insertion into the database."""
    pass
