# Import Library dan Modular Code
import pandas as pd
from utils.extract import scrape_fashion_products
from utils.transform import clean_and_transform
from utils.load import load_data

def main():
    try:
        print("Memulai proses ekstraksi data...")
        extracted_data = scrape_fashion_products(total_pages=50)
        if not extracted_data:
            print("Tidak ada data yang berhasil diambil. Proses dihentikan.")
            return

        df_raw = pd.DataFrame(extracted_data)
        print(f"Ekstraksi selesai. Jumlah data: {len(df_raw)}")

        # Menampilakan informasi dan head data sebelum transformasi
        print("\n=======Informasi Data Sebelum Transformasi:=======")
        print(df_raw.info())
        print("\n=======Data Head Sebelum Transformasi:=======")
        print(df_raw.head())

        print("\nMemulai proses transformasi data...")
        df_cleaned = clean_and_transform(df_raw)
        print(f"Transformasi selesai. Jumlah data setelah dibersihkan: {len(df_cleaned)}")

        # Menampilkan informasi dan head data setelah transformasi
        print("\n=======Informasi Data Setelah Transformasi:=======")
        print(df_cleaned.info())
        print("\n=======Data Head Setelah Transformasi:=======")
        print(df_cleaned.head())

        print("\nMemulai proses load data ke storage (CSV, PostgreSQL, Google Sheets)...")

        load_data(df=df_cleaned)
        print("Proses ETL selesai dengan sukses.")

    except Exception as e:
        print(f"Terjadi kesalahan di proses utama: {e}")

if __name__ == '__main__':
    main()
