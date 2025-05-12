import pandas as pd
from sqlalchemy import create_engine
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

def save_to_csv(df: pd.DataFrame, filename: str = 'fashion_data.csv'):
    """Menyimpan DataFrame ke file CSV."""
    try:
        df.to_csv(filename, index=False)
        print(f"[Flatfile-.CSV] Data berhasil disimpan ke {filename}")
    except Exception as e:
        print(f"[CSV Error] Gagal menyimpan data ke CSV: {e}")

def save_to_postgresql(
    df: pd.DataFrame,
    db_name: str,
    user: str,
    password: str,
    host: str = 'localhost',
    port: int = 5432,
    table_name: str = 'fashion_products'
):
    """Menyimpan DataFrame ke PostgreSQL dengan mengganti seluruh isi tabel."""
    try:
        engine = create_engine(f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{db_name}')
        df.to_sql(table_name, engine, index=False, if_exists='replace')
        print(f"[PostgreSQL] Data berhasil disimpan ke tabel {table_name}.")
    except Exception as e:
        print(f"[PostgreSQL Error] Gagal menyimpan ke PostgreSQL: {e}")

def save_to_google_spreadsheet(
    df: pd.DataFrame,
    spreadsheet_id: str,
    range_name: str,
    credential_file: str = 'client_secret.json'
):
    """Menyimpan DataFrame ke Google Spreadsheet."""
    try:
        creds = Credentials.from_service_account_file(
            credential_file,
            scopes=["https://www.googleapis.com/auth/spreadsheets"]
        )
        service = build('sheets', 'v4', credentials=creds)

        # Menghapus data lama
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range=range_name,
        ).execute()

        # Format data
        values = [df.columns.tolist()] + df.values.tolist()
        body = {'values': values}

        # Write Update ke spreadsheet
        service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="RAW",
            body=body
        ).execute()

        print(f"[Google Sheets] Data berhasil disimpan ke Spreadsheets(Pemrosesan Data Fashion).")
    except Exception as e:
        print(f"[Google Sheets Error] Gagal menyimpan ke Google Sheets: {e}")

def load_data(
    df: pd.DataFrame,
    filename_csv: str = 'fashion_data.csv',
    db_name: str = 'fashion_db',
    user: str = 'developer',
    password: str = 'supersecretpassword',
    spreadsheet_id: str = '1MDLjCAZ2eMy-FxvBpDSJfNEkTOKOVoHORcrlyT8Vu-s',
    range_name: str = 'Sheet1!A1'
):
    """Memuat data ke semua storage: CSV, PostgreSQL, dan Google Spreadsheet."""
    save_to_csv(df, filename_csv)
    save_to_postgresql(df, db_name, user, password)
    save_to_google_spreadsheet(df, spreadsheet_id, range_name)
