"""
Web scraping servisi - Mağaza sitelerinden ürün bilgilerini çeker
"""
import asyncio
import json
import time
from typing import List, Dict, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
from loguru import logger

from app.core.config import settings


class ScraperService:
    """Web scraping servisi"""
    
    def __init__(self):
        self.driver = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': settings.USER_AGENT
        })
    
    def _setup_driver(self):
        """Selenium driver'ı hazırla"""
        if self.driver is None:
            chrome_options = Options()
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument(f"--user-agent={settings.USER_AGENT}")
            
            self.driver = webdriver.Chrome(
                ChromeDriverManager().install(),
                options=chrome_options
            )
    
    def _cleanup_driver(self):
        """Driver'ı temizle"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    async def scrape_wishlist(self, store_name: str, wishlist_url: str) -> List[Dict]:
        """
        Wishlist'ten ürün bilgilerini çeker
        
        Args:
            store_name: Mağaza adı (zara, bershka, pullandbear)
            wishlist_url: Wishlist URL'i
            
        Returns:
            Ürün listesi
        """
        try:
            self._setup_driver()
            
            logger.info(f"Scraping wishlist from {store_name}: {wishlist_url}")
            
            # Sayfayı yükle
            self.driver.get(wishlist_url)
            time.sleep(settings.SCRAPING_DELAY)
            
            # Mağaza spesifik scraping
            if store_name == "zara":
                return await self._scrape_zara_wishlist()
            elif store_name == "bershka":
                return await self._scrape_bershka_wishlist()
            elif store_name == "pullandbear":
                return await self._scrape_pullandbear_wishlist()
            else:
                logger.error(f"Unsupported store: {store_name}")
                return []
                
        except Exception as e:
            logger.error(f"Error scraping wishlist from {store_name}: {str(e)}")
            return []
        finally:
            self._cleanup_driver()
    
    async def _scrape_zara_wishlist(self) -> List[Dict]:
        """Zara wishlist scraping"""
        products = []
        
        try:
            # Ürün kartlarını bul
            product_cards = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
            
            for card in product_cards:
                try:
                    product = {
                        "product_id": card.get_attribute("data-product-id") or "",
                        "product_name": "",
                        "product_url": "",
                        "product_image": "",
                        "price": "",
                        "size": "",
                        "color": "",
                        "is_in_stock": False
                    }
                    
                    # Ürün adı
                    name_elem = card.find_element(By.CSS_SELECTOR, ".product-name")
                    if name_elem:
                        product["product_name"] = name_elem.text.strip()
                    
                    # Ürün URL'i
                    link_elem = card.find_element(By.CSS_SELECTOR, "a")
                    if link_elem:
                        product["product_url"] = link_elem.get_attribute("href")
                    
                    # Ürün resmi
                    img_elem = card.find_element(By.CSS_SELECTOR, "img")
                    if img_elem:
                        product["product_image"] = img_elem.get_attribute("src")
                    
                    # Fiyat
                    price_elem = card.find_element(By.CSS_SELECTOR, ".price")
                    if price_elem:
                        product["price"] = price_elem.text.strip()
                    
                    # Stok durumu
                    stock_elem = card.find_element(By.CSS_SELECTOR, ".product-availability")
                    if stock_elem:
                        product["is_in_stock"] = "stokta" in stock_elem.text.lower()
                    
                    products.append(product)
                    
                except NoSuchElementException:
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping Zara wishlist: {str(e)}")
        
        return products
    
    async def _scrape_bershka_wishlist(self) -> List[Dict]:
        """Bershka wishlist scraping"""
        products = []
        
        try:
            # Bershka için benzer scraping mantığı
            product_cards = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
            
            for card in product_cards:
                try:
                    product = {
                        "product_id": card.get_attribute("data-product-id") or "",
                        "product_name": "",
                        "product_url": "",
                        "product_image": "",
                        "price": "",
                        "size": "",
                        "color": "",
                        "is_in_stock": False
                    }
                    
                    # Bershka spesifik selectors
                    name_elem = card.find_element(By.CSS_SELECTOR, ".product-name")
                    if name_elem:
                        product["product_name"] = name_elem.text.strip()
                    
                    link_elem = card.find_element(By.CSS_SELECTOR, "a")
                    if link_elem:
                        product["product_url"] = link_elem.get_attribute("href")
                    
                    products.append(product)
                    
                except NoSuchElementException:
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping Bershka wishlist: {str(e)}")
        
        return products
    
    async def _scrape_pullandbear_wishlist(self) -> List[Dict]:
        """Pull&Bear wishlist scraping"""
        products = []
        
        try:
            # Pull&Bear için benzer scraping mantığı
            product_cards = self.driver.find_elements(By.CSS_SELECTOR, ".product-item")
            
            for card in product_cards:
                try:
                    product = {
                        "product_id": card.get_attribute("data-product-id") or "",
                        "product_name": "",
                        "product_url": "",
                        "product_image": "",
                        "price": "",
                        "size": "",
                        "color": "",
                        "is_in_stock": False
                    }
                    
                    # Pull&Bear spesifik selectors
                    name_elem = card.find_element(By.CSS_SELECTOR, ".product-name")
                    if name_elem:
                        product["product_name"] = name_elem.text.strip()
                    
                    link_elem = card.find_element(By.CSS_SELECTOR, "a")
                    if link_elem:
                        product["product_url"] = link_elem.get_attribute("href")
                    
                    products.append(product)
                    
                except NoSuchElementException:
                    continue
                    
        except Exception as e:
            logger.error(f"Error scraping Pull&Bear wishlist: {str(e)}")
        
        return products
    
    async def check_product_stock(self, product_url: str, store_name: str) -> Dict:
        """
        Tek bir ürünün stok durumunu kontrol eder
        
        Args:
            product_url: Ürün URL'i
            store_name: Mağaza adı
            
        Returns:
            Stok durumu bilgisi
        """
        try:
            self._setup_driver()
            
            logger.info(f"Checking stock for product: {product_url}")
            
            self.driver.get(product_url)
            time.sleep(settings.SCRAPING_DELAY)
            
            stock_info = {
                "is_in_stock": False,
                "available_sizes": [],
                "available_colors": [],
                "price": None,
                "last_checked": None
            }
            
            # Mağaza spesifik stok kontrolü
            if store_name == "zara":
                return await self._check_zara_stock()
            elif store_name == "bershka":
                return await self._check_bershka_stock()
            elif store_name == "pullandbear":
                return await self._check_pullandbear_stock()
            
        except Exception as e:
            logger.error(f"Error checking stock for {product_url}: {str(e)}")
            return {"is_in_stock": False, "error": str(e)}
        finally:
            self._cleanup_driver()
    
    async def _check_zara_stock(self) -> Dict:
        """Zara stok kontrolü"""
        try:
            # Stok durumu
            stock_elem = self.driver.find_element(By.CSS_SELECTOR, ".product-availability")
            is_in_stock = "stokta" in stock_elem.text.lower() if stock_elem else False
            
            # Mevcut bedenler
            sizes = []
            size_elems = self.driver.find_elements(By.CSS_SELECTOR, ".size-selector .size")
            for size_elem in size_elems:
                if "disabled" not in size_elem.get_attribute("class"):
                    sizes.append(size_elem.text.strip())
            
            # Fiyat
            price_elem = self.driver.find_element(By.CSS_SELECTOR, ".price")
            price = price_elem.text.strip() if price_elem else None
            
            return {
                "is_in_stock": is_in_stock,
                "available_sizes": sizes,
                "available_colors": [],
                "price": price,
                "last_checked": None
            }
            
        except Exception as e:
            logger.error(f"Error checking Zara stock: {str(e)}")
            return {"is_in_stock": False, "error": str(e)}
    
    async def _check_bershka_stock(self) -> Dict:
        """Bershka stok kontrolü"""
        # Bershka için benzer mantık
        return {"is_in_stock": False, "available_sizes": [], "available_colors": []}
    
    async def _check_pullandbear_stock(self) -> Dict:
        """Pull&Bear stok kontrolü"""
        # Pull&Bear için benzer mantık
        return {"is_in_stock": False, "available_sizes": [], "available_colors": []}


# Global scraper instance
scraper_service = ScraperService() 