import pytest
import pandas as pd
from unittest.mock import patch, MagicMock
import sys
import os

# Menambahkan path agar bisa import utils
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.load import (
    save_to_csv,
    save_to_postgresql,
    save_to_google_spreadsheet,
    load_data
)

# Fixture DataFrame
@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "Title": ["Item A"],
        "Price": [160000.0],
        "Rating": [4.5],
        "Colors": [3],
        "Size": ["M"],
        "Gender": ["Male"],
        "Timestamp": ["2025-05-10T10:00:00.000000"]
    })

# Test Fungsi Flatfile menyimpan ke .CSV
def test_save_to_csv(tmp_path, sample_dataframe):
    file_path = tmp_path / "test_fashion.csv"
    save_to_csv(sample_dataframe, filename=str(file_path))

    assert file_path.exists()
    df_read = pd.read_csv(file_path)
    assert not df_read.empty
    assert list(df_read.columns) == list(sample_dataframe.columns)


# Test untuk menangani Exception di save_to_csv
@patch("pandas.DataFrame.to_csv", side_effect=Exception("Disk penuh"))
def test_save_to_csv_exception(mock_to_csv, capsys, sample_dataframe):
    # Memanggil fungsi save_to_csv dengan DataFrame yang valid
    save_to_csv(sample_dataframe, filename="test_fashion.csv")
    
    # Menangkap output yang dicetak ke console
    captured = capsys.readouterr()
    
    # Memastikan bahwa pesan error yang benar tercetak
    assert "[CSV Error] Gagal menyimpan data ke CSV: Disk penuh" in captured.out

# Test Fungsi save_to_postgresql (normal)
@patch("utils.load.create_engine")
def test_save_to_postgresql(mock_create_engine, sample_dataframe):
    mock_engine = MagicMock()
    mock_create_engine.return_value = mock_engine

    sample_dataframe.to_sql = MagicMock()

    save_to_postgresql(
        df=sample_dataframe,
        db_name="test_db",
        user="user",
        password="password"
    )

    sample_dataframe.to_sql.assert_called_once_with("fashion_products", mock_engine, index=False, if_exists="replace")

# Test Fungsi save_to_postgresql (exception)
@patch("utils.load.create_engine", side_effect=Exception("Connection failed"))
def test_save_to_postgresql_exception(mock_create_engine, sample_dataframe, capsys):
    save_to_postgresql(
        df=sample_dataframe,
        db_name="invalid_db",
        user="invalid_user",
        password="invalid_pass"
    )
    captured = capsys.readouterr()
    assert "[PostgreSQL Error]" in captured.out

# Test Fungsi save_to_google_spreadsheet (normal)
@patch("utils.load.Credentials.from_service_account_file")
@patch("utils.load.build")
def test_save_to_google_spreadsheet(mock_build, mock_creds, sample_dataframe):
    mock_service = MagicMock()
    mock_spreadsheets = MagicMock()
    mock_values = MagicMock()

    mock_service.spreadsheets.return_value = mock_spreadsheets
    mock_spreadsheets.values.return_value = mock_values
    mock_values.clear.return_value.execute.return_value = None
    mock_values.update.return_value.execute.return_value = None

    mock_build.return_value = mock_service

    save_to_google_spreadsheet(
        df=sample_dataframe,
        spreadsheet_id="fake_id",
        range_name="Sheet1!A1",
        credential_file="fake_credential.json"
    )

    mock_creds.assert_called_once()
    mock_build.assert_called_once_with("sheets", "v4", credentials=mock_creds.return_value)
    assert mock_values.clear.called
    assert mock_values.update.called

# Test Fungsi save_to_google_spreadsheet (exception)
@patch("utils.load.Credentials.from_service_account_file", side_effect=Exception("Invalid credentials"))
def test_save_to_google_spreadsheet_exception(mock_creds, sample_dataframe, capsys):
    save_to_google_spreadsheet(
        df=sample_dataframe,
        spreadsheet_id="invalid_id",
        range_name="Sheet1!A1",
        credential_file="fake_credential.json"
    )
    captured = capsys.readouterr()
    assert "[Google Sheets Error]" in captured.out

# Test Fungsi load_data (semua storage)
@patch("utils.load.save_to_csv")
@patch("utils.load.save_to_postgresql")
@patch("utils.load.save_to_google_spreadsheet")
def test_load_data(mock_gsheet, mock_postgres, mock_csv, sample_dataframe):
    load_data(sample_dataframe)
    mock_csv.assert_called_once()
    mock_postgres.assert_called_once()
    mock_gsheet.assert_called_once()
