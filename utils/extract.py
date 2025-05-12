import time
from datetime import datetime
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
    )
}

def fetching_content(url: str):
    """Mengambil konten dari URL dengan penanganan kesalahan jaringan."""
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  # status code sukses
        return response.content
    except requests.RequestException as e:
        print(f"Error fetching content from {url}: {e}")
        return None


def extract_clean_text(info_list, keyword, pattern, default="N/A"):
    """Mengekstraksi teks yang bersih berdasarkan pola dan kata kunci."""
    for p in info_list:
        if p.string and keyword in p.string:
            match = re.search(pattern, p.string)
            if match:
                return match.group(1).strip()
    return default


def extract_product_data(card):
    """Mengambil data produk dari elemen dengan class 'collection-card'."""
    try:
        # Title
        title_element = card.select_one('.product-details h3.product-title')
        title = title_element.text.strip() if title_element and title_element.text.strip() else "Unknown Title"

        # Price
        price_element = card.find('div', class_='price-container')
        price = price_element.text.strip() if price_element else "Price Not Available"

        # Info Paragraf
        info_paragraphs = card.find_all('p')

        rating = extract_clean_text(info_paragraphs, "Rating", r"Rating:\s*(⭐\s*\d+(?:\.\d+)?)", "Invalid Rating")
        colors = extract_clean_text(info_paragraphs, "Colors", r"(\d+)\s*Colors", "No Colors")
        size = extract_clean_text(info_paragraphs, "Size", r"Size:\s*(\w+)", "Unknown")
        gender = extract_clean_text(info_paragraphs, "Gender", r"Gender:\s*(\w+)", "Unknown")

        # Timestamp waktu pengambilan data
        timestamp = datetime.now()

        # Mengembalikan hasil ekstraksi sebagai dictionary
        return {
            "Title": title,
            "Price": price,
            "Rating": rating,
            "Colors": colors,
            "Size": size,
            "Gender": gender,
            "Timestamp": timestamp
        }

    except Exception as e:
        print(f"Terjadi kesalahan saat mengekstrak data produk: {e}")
        return None


def scrape_fashion_products(total_pages, delay=2):
    """Scraping data fashion dari beberapa halaman dan menyimpannya ke list dengan penanganan kesalahan."""
    data = []
    for page_number in range(1, total_pages + 1):
        if page_number == 1:
            url = 'https://fashion-studio.dicoding.dev/'
        else:
            url = f'https://fashion-studio.dicoding.dev/page{page_number}'
        
        print(f"Scraping halaman: {url}")
        content = fetching_content(url)

        if content:
            try:
                # Parsing HTML dengan BeautifulSoup
                soup = BeautifulSoup(content, "html.parser")
                cards = soup.find_all('div', class_='collection-card')
                if not cards:
                    print(f"Tidak ada produk ditemukan di halaman {page_number}.")
                    continue  # Jika tidak ada produk, maka akan melanjutkan ke halaman berikutnya
                
                for card in cards:
                    try:
                        product = extract_product_data(card)
                        if product:
                            data.append(product)
                    except Exception as e:
                        print(f"Terjadi kesalahan saat mengekstrak data produk pada halaman {page_number}: {e}")
                time.sleep(delay)  # Delay antar halaman 
            except Exception as e:
                print(f"Terjadi kesalahan saat parsing halaman {page_number}: {e}")
                continue  # Jika terjadi kesalahan parsing, maka akan melanjutkan ke halaman berikutnya
        else:
            print(f"Gagal mengambil data dari halaman {page_number}, berhenti scraping.")
            break  # Jika gagal fetching, maka akan menghentikan proses

    return data

