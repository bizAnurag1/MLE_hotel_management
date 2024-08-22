import pytest
from unittest.mock import patch, MagicMock
from bill_generator import Restaurant
import datetime

@pytest.fixture
def restaurant():
    return Restaurant(tbl_id=1)

@patch('bill_generator.db_connection')
def test_check_menu_availability(mock_db, Restaurant):
    # Mocking the database cursor and its fetchone method
    mock_cursor = MagicMock()
    mock_cursor.fetchone.return_value = ('Y',)
    mock_db.return_value.__enter__.return_value = mock_cursor

    available = Restaurant.check_menu_availability(menu_id=101)
    
    assert available is True
    mock_cursor.execute.assert_called_once_with(
        "SELECT Available FROM restaurant.Menu_card WHERE menu_id = ?", (101,)
    )