from pathlib import Path
from core_gui_atomistic.periodic_table import TPeriodTable
import pytest


@pytest.fixture
def period_table() -> TPeriodTable:
    return TPeriodTable()
