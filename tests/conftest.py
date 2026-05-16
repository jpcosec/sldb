import os


def pytest_configure():
    os.environ.setdefault("SLDB_SUPPRESS_DEPRECATION", "1")
