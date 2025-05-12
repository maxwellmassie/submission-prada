# Submission Proyek Akhir: Membangun ETL Pipeline Sederhana

Proyek ini merupakan implementasi pipeline **ETL (Extract, Transform, Load)** untuk mengambil data produk fashion dari web [Fashion Studio Dicoding](https://fashion-studio.dicoding.dev/), membersihkannya, dan menyimpannya ke dalam tiga storage sekaligus: **CSV**, **PostgreSQL**, dan **Google Spreadsheet**.

---

## 🧩 Fitur

### 🔍 Extract
Mengambil data HTML produk fashion dari website menggunakan `requests` dan `BeautifulSoup`.

### 🔧 Transform
Membersihkan dan mengubah data:
- Kolom `Price` dikonversi menjadi *float* dalam mata uang Rupiah (kurs: Rp16.000).
- Kolom `Rating` diubah menjadi *float*, menghilangkan nilai seperti "Invalid Rating" atau "4.8 / 5".
- Kolom `Colors` dikonversi ke integer (contoh: "3 Colors" → `3`).
- Kolom `Size` disederhanakan menjadi ukuran saja (tanpa teks "Size: ").
- Kolom `Gender` disederhanakan menjadi jenis kelamin saja (tanpa teks "Gender: ").
- Menambahkan kolom baru bernama `timestamp` yang menginformasikan waktu tahapan ekstraksi (web scraping). 

### 💾 Load
- Menyimpan hasil transformasi ke file **CSV** lokal.
- Menyimpan ke **PostgreSQL database**.
- Menyimpan ke **Google Spreadsheet** (dengan integrasi Google Sheets API).

---

## 📁 Struktur Proyek
```
├── screenshoot
│ ├── PostgreSql.png
│ ├── spreadsheet.png
│ └── TerimalVscode.png
├── tests
│ ├── test_extract.py
│ ├── test_transform.py
│ └── test_load.py
├── utils
│ ├── extract.py
│ ├── transform.py
│ └── load.py
├── main.py
├── requirements.txt
├── submission.txt
├── products.csv
└── README.md
```
---
## ⚙ Teknologi yang Digunakan
- Python 3.9.13
- BeautifulSoup
- Pandas
- SQLAlchemy
- Google Sheets API
- PostgreSQL
- Pytest, Pytest-Cov

---
## 📤 Output

- **File CSV**: `fashion_data.csv`
- **PostgreSQL**: Database `fashion_db`, Tabel `fashion_products`
- **Google Spreadsheet**: [Link Spreadsheet](https://docs.google.com/spreadsheets/d/1MDLjCAZ2eMy-FxvBpDSJfNEkTOKOVoHORcrlyT8Vu-s/edit?gid=0#gid=0)

---

## 💻 Output di Terminal (ETL Berhasil)
```
Memulai proses ekstraksi data...
Scraping halaman: https://fashion-studio.dicoding.dev/
.....
Scraping halaman: https://fashion-studio.dicoding.dev/page50
Ekstraksi selesai. Jumlah data: 1000

=======Informasi Data Sebelum Transformasi:=======
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 1000 entries, 0 to 999
Data columns (total 7 columns):
 #   Column     Non-Null Count  Dtype
---  ------     --------------  -----
 0   Title      1000 non-null   object
 1   Price      1000 non-null   object
 2   Rating     1000 non-null   object
 3   Colors     1000 non-null   object
 4   Size       1000 non-null   object
 5   Gender     1000 non-null   object
 6   Timestamp  1000 non-null   datetime64[ns]
dtypes: datetime64[ns](1), object(6)
memory usage: 54.8+ KB
None

=======Data Head Sebelum Transformasi:=======
             Title    Price          Rating Colors Size  Gender                  Timestamp
0  Unknown Product  $100.00  Invalid Rating      5    M     Men 2025-05-12 21:55:46.510667
1        T-shirt 2  $102.15           ⭐ 3.9      3    M   Women 2025-05-12 21:55:46.510667
2         Hoodie 3  $496.88           ⭐ 4.8      3    L  Unisex 2025-05-12 21:55:46.510667
3          Pants 4  $467.31           ⭐ 3.3      3   XL     Men 2025-05-12 21:55:46.510667
4      Outerwear 5  $321.59           ⭐ 3.5      3  XXL   Women 2025-05-12 21:55:46.510667

Memulai proses transformasi data...
Transformasi selesai. Jumlah data setelah dibersihkan: 867

=======Informasi Data Setelah Transformasi:=======
<class 'pandas.core.frame.DataFrame'>
Index: 867 entries, 1 to 999
Data columns (total 7 columns):
 #   Column     Non-Null Count  Dtype
---  ------     --------------  -----
 0   Title      867 non-null    object
 1   Price      867 non-null    float64
 2   Rating     867 non-null    float64
 3   Colors     867 non-null    int64
 4   Size       867 non-null    object
 5   Gender     867 non-null    object
 6   Timestamp  867 non-null    object
dtypes: float64(2), int64(1), object(4)
memory usage: 54.2+ KB
None

=======Data Head Setelah Transformasi:=======
         Title      Price  Rating  Colors Size  Gender                   Timestamp
1    T-shirt 2  1634400.0     3.9       3    M   Women  2025-05-12T21:55:46.510667
2     Hoodie 3  7950080.0     4.8       3    L  Unisex  2025-05-12T21:55:46.510667
3      Pants 4  7476960.0     3.3       3   XL     Men  2025-05-12T21:55:46.510667
4  Outerwear 5  5145440.0     3.5       3  XXL   Women  2025-05-12T21:55:46.510667
5     Jacket 6  2453920.0     3.3       3    S  Unisex  2025-05-12T21:55:46.511666

Memulai proses load data ke storage (CSV, PostgreSQL, Google Sheets)...
[Flatfile-.CSV] Data berhasil disimpan ke fashion_data.csv
[PostgreSQL] Data berhasil disimpan ke tabel fashion_products.
[Google Sheets] Data berhasil disimpan ke Spreadsheets(Pemrosesan Data Fashion).
Proses ETL selesai dengan sukses.
```
---
## Test Coverage 📊
Test coverage untuk folder tests/pengujian berada pada **95%**.
```
File	                  statements	missing	excluded	coverage
--------------------------------------------------------------------
tests\test_extract.py	         104	      1	       0	     99%
tests\test_load.py	              63	      0	       0	    100%
tests\test_transform.py	          27	      0	       0	    100%
utils\extract.py	              67	     13	       0	     81%
utils\load.py	                  32	      0	       0	    100%
utils\transform.py	              17	      0	       0	    100%
--------------------------------------------------------------------
Total	                         310	     14	       0	     95%
-----------------------------------------------------
coverage.py v7.8.0, created at 2025-05-12 22:01 +0700
```
---
## 🚀 Instalasi
1. **Clone repositori ini atau unduh sebagai ZIP**:
   ```bash
   git clone https://github.com/maxwellmassie/submission-prada.git
2.  **Membuat Virtual Environment**:
    ```bash
    python -m venv .env
    ```
3.  **Mengaktifkan Virtual Environment**:
    -   **Windows**:
        ```bash
        .env\Scripts\activate
        ```
4.  **Menginstall Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
5.  **Konfigurasi PostgreSQL** pada `utils/load.py`:
    Sesuaikan konfigurasi database PostgreSQL Anda:
    ```python
    db_name: str = 'fashion_db'
    user: str = 'xxxxxxxx'
    password: str = 'xxxxxxxxx'
    ```
## ▶ Menjalankan Proyek:

1.  **Jalankan Proses ETL**:
    ```bash
    python main.py
    ```

2.  **Menjalankan Unit Test**:
    ```bash
    python -m pytest tests
    ```

3.  **Menjalankan Test Coverage**:
    ```bash
    python -m pytest tests -v --cov --cov-report=html
    ```
---
Terima kasih telah membaca dokumentasi ini🙏 

Salam hangat,
Maxwell Massie