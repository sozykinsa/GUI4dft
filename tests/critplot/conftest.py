from pathlib import Path
from core_atomistic.periodic_table import TPeriodTable

import pytest


@pytest.fixture
def tests_path() -> Path:
    return Path(__file__).parent


@pytest.fixture
def period_table() -> TPeriodTable:
    return TPeriodTable()
