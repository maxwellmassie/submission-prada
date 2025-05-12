import pandas as pd

def clean_and_transform(df: pd.DataFrame) -> pd.DataFrame:
    """Transformasi data hasil ekstraksi agar siap untuk dimuat ke storage dengan penanganan kesalahan."""

    try:
        # Menghapus baris dengan rating invalid
        df = df[df['Rating'] != 'Invalid Rating'].copy()

        # Membersihkan dan mengonversi kolom Rating ke float
        df['Rating'] = df['Rating'].str.extract(r'⭐\s*(\d+\.\d+)')
        df['Rating'] = df['Rating'].astype(float)

        # Membersihkan dan mengonversi kolom Price ke float, lalu ke rupiah
        df['Price'] = df['Price'].str.replace('$', '', regex=False).str.replace(',', '', regex=False)
        df['Price'] = df['Price'].astype(float) * 16000
        df['Price'] = df['Price'].round(1).astype('float64')

        # mengonversi Colors menjadi integer
        df['Colors'] = df['Colors'].str.extract(r'(\d+)').astype(int)

        # mengonversi Size dan Gender menjadi string
        df['Size'] = df['Size'].astype(str)
        df['Gender'] = df['Gender'].astype(str)

        # Formating Timetamp
        df['Timestamp'] = pd.to_datetime(df['Timestamp'], errors='coerce').dt.strftime('%Y-%m-%dT%H:%M:%S.%f')

    except Exception as e:
        print(f"[Transform Error] Terjadi kesalahan saat transformasi data: {e}")
        return pd.DataFrame()  # Mengembalikan DataFrame kosong jika error

    return df
