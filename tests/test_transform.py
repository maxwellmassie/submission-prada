import pytest
import pandas as pd
from utils.transform import clean_and_transform
import sys
import os

# Menambahkan direktori parent ke dalam path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def test_clean_and_transform_valid_data():
    data = {
        "Title": ["Item A", "Item B"],
        "Price": ["$10.00", "$20.00"],
        "Rating": ["⭐ 4.5", "⭐ 3.9"],
        "Colors": ["3 Colors", "5 Colors"],
        "Size": ["M", "L"],
        "Gender": ["Male", "Female"],
        "Timestamp": ["2025-05-10 10:00:00", "2025-05-10 11:00:00"]
    }
    df = pd.DataFrame(data)
    result = clean_and_transform(df)

    assert not result.empty
    assert result["Rating"].dtype == float
    assert result["Price"].dtype == float
    assert result["Colors"].dtype == int
    assert pd.api.types.is_string_dtype(result["Size"])
    assert pd.api.types.is_string_dtype(result["Gender"])
    assert result["Timestamp"].str.contains("T").all()  # Format ISO

def test_clean_and_transform_invalid_rating():
    data = {
        "Title": ["Item A"],
        "Price": ["$10.00"],
        "Rating": ["Invalid Rating"],
        "Colors": ["3 Colors"],
        "Size": ["M"],
        "Gender": ["Male"],
        "Timestamp": ["2025-05-10 10:00:00"]
    }
    df = pd.DataFrame(data)
    result = clean_and_transform(df)

    # baris dihapus dan DataFrame kosong
    assert result.empty

def test_clean_and_transform_malformed_price():
    data = {
        "Title": ["Item A"],
        "Price": ["INVALID"],
        "Rating": ["⭐ 4.0"],
        "Colors": ["3 Colors"],
        "Size": ["M"],
        "Gender": ["Male"],
        "Timestamp": ["2025-05-10 10:00:00"]
    }
    df = pd.DataFrame(data)
    result = clean_and_transform(df)

    # jika konversi Price akan gagal, maka fungsi akan mengembalikan DataFrame kosong
    assert result.empty
