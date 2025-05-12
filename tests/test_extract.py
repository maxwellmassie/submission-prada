import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Menambahkan direktori parent ke dalam path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.extract import fetching_content, extract_clean_text, extract_product_data, scrape_fashion_products, HEADERS
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import time

class TestExtractFunctions(unittest.TestCase):

    @patch('utils.extract.requests.get')
    def test_fetching_content_returns_content_on_success(self, mock_get):
        """Uji untuk memastikan fetching_content mengembalikan konten saat respon HTTP sukses (status code 200)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"<html><body>Test Content</body></html>"
        mock_get.return_value = mock_response
        url = "http://example.com"
        content = fetching_content(url)
        self.assertEqual(content, b"<html><body>Test Content</body></html>")
        mock_get.assert_called_once_with(url, headers=HEADERS)

    @patch('utils.extract.requests.get')
    def test_fetching_content_returns_none_on_failure(self, mock_get):
        """Uji untuk memastikan fetching_content mengembalikan None saat permintaan HTTP gagal (RequestException)."""
        mock_response = MagicMock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("HTTP Error")
        mock_get.return_value = mock_response
        url = "http://example.com/error"
        content = fetching_content(url)
        self.assertIsNone(content)
        mock_get.assert_called_once_with(url, headers=HEADERS)

    def test_extract_clean_text_finds_text(self):
        """Uji untuk memastikan extract_clean_text berhasil mengekstrak teks yang sesuai jika ditemukan."""
        info_list = [MagicMock(string="Rating: ⭐ 4.5"), MagicMock(string="Colors: 3 Colors")]
        keyword = "Rating"
        pattern = r"Rating:\s*(⭐\s*\d+(?:\.\d+)?)"
        result = extract_clean_text(info_list, keyword, pattern)
        self.assertEqual(result, "⭐ 4.5")

    def test_extract_clean_text_returns_na_if_not_found(self):
        """Uji untuk memastikan extract_clean_text mengembalikan 'N/A' jika kata kunci tidak ditemukan."""
        info_list = [MagicMock(string="Colors: 3 Colors"), MagicMock(string="Size: M")]
        keyword = "Rating"
        pattern = r"Rating:\s*(⭐\s*\d+(?:\.\d+)?)"
        result = extract_clean_text(info_list, keyword, pattern)
        self.assertEqual(result, "N/A")

    def test_extract_clean_text_returns_na_if_no_match(self):
        """Uji untuk memastikan extract_clean_text mengembalikan 'N/A' jika pola tidak cocok."""
        info_list = [MagicMock(string="Rating Text"), MagicMock(string="Colors: 3 Colors")]
        keyword = "Rating"
        pattern = r"Rating:\s*(⭐\s*\d+(?:\.\d+)?)"
        result = extract_clean_text(info_list, keyword, pattern)
        self.assertEqual(result, "N/A")

    def test_extract_clean_text_returns_default_value(self):
        """Uji untuk memastikan extract_clean_text mengembalikan nilai default jika kata kunci tidak ditemukan."""
        info_list = [MagicMock(string="Some other info")]
        keyword = "NonExistent"
        pattern = r"NonExistent:\s*(.*)"
        default_value = "Not Found"
        result = extract_clean_text(info_list, keyword, pattern, default_value)
        self.assertEqual(result, "Not Found")

    def test_extract_product_data_success(self):
        """Uji untuk memastikan extract_product_data berhasil mengekstrak informasi produk dengan benar."""
        html_content = """
            <div class="collection-card">
                <div class="product-details">
                    <h3 class="product-title">Test Product</h3>
                </div>
                <div class="price-container">$25.00</div>
                <p>Rating: ⭐ 4.8</p>
                <p>Colors: 2 Colors</p>
                <p>Size: L</p>
                <p>Gender: Female</p>
            </div>
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        card = soup.find('div', class_='collection-card')
        product_data = extract_product_data(card)
        self.assertEqual(product_data['Title'], "Test Product")
        self.assertEqual(product_data['Price'], "$25.00")
        self.assertEqual(product_data['Rating'], "⭐ 4.8")
        self.assertEqual(product_data['Colors'], "2")
        self.assertEqual(product_data['Size'], "L")
        self.assertEqual(product_data['Gender'], "Female")
        self.assertIsInstance(product_data['Timestamp'], datetime)

    def test_extract_product_data_handles_missing_elements(self):
        """Uji untuk memastikan extract_product_data menangani elemen HTML yang hilang dengan baik."""
        html_content = """
            <div class="collection-card">
                <div class="product-details">
                    <h3 class="product-title">Another Product</h3>
                </div>
            </div>
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        card = soup.find('div', class_='collection-card')
        product_data = extract_product_data(card)
        self.assertEqual(product_data['Title'], "Another Product")
        self.assertEqual(product_data['Price'], "Price Not Available")
        self.assertEqual(product_data['Rating'], "Invalid Rating")
        self.assertEqual(product_data['Colors'], "No Colors")
        self.assertEqual(product_data['Size'], "Unknown")
        self.assertEqual(product_data['Gender'], "Unknown")
        self.assertIsInstance(product_data['Timestamp'], datetime)

    def test_extract_product_data_handles_empty_title(self):
        """Uji untuk memastikan extract_product_data menangani produk dengan judul kosong."""
        html_content = """
            <div class="collection-card">
                <div class="product-details">
                    <h3 class="product-title"></h3>
                </div>
                <div class="price-container">$30.00</div>
                <p>Rating: ⭐ 4.0</p>
            </div>
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        card = soup.find('div', class_='collection-card')
        product_data = extract_product_data(card)
        self.assertEqual(product_data['Title'], "Unknown Title")
        self.assertEqual(product_data['Price'], "$30.00")
        self.assertEqual(product_data['Rating'], "⭐ 4.0")

    @patch('utils.extract.fetching_content')
    @patch('utils.extract.extract_product_data')
    @patch('utils.extract.time.sleep')
    def test_scrape_fashion_products_single_page_success(self, mock_sleep, mock_extract, mock_fetch):
        """Uji untuk memastikan scraping produk dari satu halaman berjalan sukses."""
        mock_fetch.return_value = b"""
            <html><body>
                <div class="collection-card"></div>
            </body></html>
        """
        mock_soup = MagicMock()
        mock_soup.find_all.return_value = [MagicMock()]
        with patch('bs4.BeautifulSoup', return_value=mock_soup):
            mock_extract.return_value = {"Title": "Test", "Price": "$10"}
            data = scrape_fashion_products(1, delay=0.1)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['Title'], "Test")
            mock_fetch.assert_called_once_with('https://fashion-studio.dicoding.dev/')
            mock_extract.assert_called_once()
            mock_sleep.assert_called_once_with(0.1)


if __name__ == '__main__':
    unittest.main()
