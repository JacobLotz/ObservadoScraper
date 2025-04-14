import datetime
import calendar
import pytest
from unittest.mock import patch, MagicMock
import numpy as np
import matplotlib.pyplot as plt

from scripts.migrationtrendfun import GetMonthEnd, GetStartDates, GetEndDates, DivideChunks, GetSpeciesPlot
from classes import *

import numpy as np

def test_GetMonthEnd():
    assert GetMonthEnd(datetime.date(2024, 1, 15)) == 31
    assert GetMonthEnd(datetime.date(2024, 2, 1)) == 29  # Leap year
    assert GetMonthEnd(datetime.date(2023, 2, 1)) == 28
    assert GetMonthEnd(datetime.date(2024, 4, 1)) == 30

def test_GetStartDates():
    result = GetStartDates(1, 1, 2024)
    expected = [
        datetime.date(2024, 1, 1),
        datetime.date(2024, 1, 11),
        datetime.date(2024, 1, 21),
    ]
    assert result == expected

def test_GetEndDates():
    result = GetEndDates(1, 1, 2024)
    expected = [
        datetime.date(2024, 1, 11),
        datetime.date(2024, 1, 21),
        datetime.date(2024, 1, 31),
    ]
    assert result == expected

def test_DivideChunks_even_split():
    data = [1, 2, 3, 4, 5, 6]
    chunks = list(DivideChunks(data, 2))
    assert chunks == [[1, 2], [3, 4], [5, 6]]

def test_DivideChunks_uneven_split():
    data = [1, 2, 3, 4, 5]
    chunks = list(DivideChunks(data, 2))
    assert chunks == [[1, 2], [3, 4], [5]]

