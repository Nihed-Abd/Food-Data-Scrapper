#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import csv
import time
import random
import os
from tqdm import tqdm
import pandas as pd

class FoodScraper:
    def __init__(self, target_count=2000, output_file="food_data.csv"):
        self.target_count = target_count
        self.output_file = output_file
        self.base_url = "https://world.openfoodfacts.org/api/v2/product"
        self.user_agent = "FoodNutritionScraper/1.0 (data collection for research project)"
        self.headers = {"User-Agent": self.user_agent}
        self.fields = [
            "id_produit", "nom_produit", "marque", "categorie", "sous_categorie",
            "type_emballage", "poids_net", "volume", "energie_kcal", "energie_kj",
            "lipides", "acides_gras_satures", "acides_gras_mono_insatures", 
            "acides_gras_poly_insatures", "cholesterol", "glucides", "sucres", 
            "amidon", "fibres_alimentaires", "proteines", "sel", "sodium", 
            "calcium", "fer", "magnesium", "zinc", "vitamine_a", "vitamine_c", 
            "vitamine_d", "vitamine_b1", "vitamine_b2", "vitamine_b3", "vitamine_b6", 
            "vitamine_b12", "vitamine_e", "vitamine_k", "omega_3", "omega_6", 
            "ingredients", "additifs", "allergenes", "certifications", "pays_origine", 
            "lieu_fabrication", "instructions_conservation", "mode_preparation", 
            "date_expiration", "code_barres", "site_internet_marque", "service_client_contact"
        ]
        self.products = []
        
    def _extract_nutrient(self, nutriments, nutrient_id, unit=""):
        """Extract nutrient value with its unit if available"""
        if nutrient_id in nutriments:
            value = nutriments.get(nutrient_id)
            if value is not None:
                if unit and isinstance(value, (int, float)):
                    return f"{value}{unit}"
                return value
        return ""
    
    def _get_field_value(self, product, field_name):
        """Extract the requested field from the product data"""
        if not product:
            return ""
            
        nutriments = product.get("nutriments", {})
        
        # Mapping of field names to extraction logic
        field_mapping = {
            "id_produit": product.get("_id", ""),
            "nom_produit": product.get("product_name", ""),
            "marque": ", ".join(product.get("brands_tags", [])),
            "categorie": ", ".join(product.get("categories_tags", [])),
            "sous_categorie": ", ".join(product.get("categories_tags", [])[1:] if len(product.get("categories_tags", [])) > 1 else []),
            "type_emballage": ", ".join(product.get("packaging_tags", [])),
            "poids_net": product.get("quantity", ""),
            "volume": self._extract_volume(product),
            "energie_kcal": self._extract_nutrient(nutriments, "energy-kcal", " kcal"),
            "energie_kj": self._extract_nutrient(nutriments, "energy-kj", " kJ"),
            "lipides": self._extract_nutrient(nutriments, "fat", "g"),
            "acides_gras_satures": self._extract_nutrient(nutriments, "saturated-fat", "g"),
            "acides_gras_mono_insatures": self._extract_nutrient(nutriments, "monounsaturated-fat", "g"),
            "acides_gras_poly_insatures": self._extract_nutrient(nutriments, "polyunsaturated-fat", "g"),
            "cholesterol": self._extract_nutrient(nutriments, "cholesterol", "mg"),
            "glucides": self._extract_nutrient(nutriments, "carbohydrates", "g"),
            "sucres": self._extract_nutrient(nutriments, "sugars", "g"),
            "amidon": self._extract_nutrient(nutriments, "starch", "g"),
            "fibres_alimentaires": self._extract_nutrient(nutriments, "fiber", "g"),
            "proteines": self._extract_nutrient(nutriments, "proteins", "g"),
            "sel": self._extract_nutrient(nutriments, "salt", "g"),
            "sodium": self._extract_nutrient(nutriments, "sodium", "mg"),
            "calcium": self._extract_nutrient(nutriments, "calcium", "mg"),
            "fer": self._extract_nutrient(nutriments, "iron", "mg"),
            "magnesium": self._extract_nutrient(nutriments, "magnesium", "mg"),
            "zinc": self._extract_nutrient(nutriments, "zinc", "mg"),
            "vitamine_a": self._extract_nutrient(nutriments, "vitamin-a", "µg"),
            "vitamine_c": self._extract_nutrient(nutriments, "vitamin-c", "mg"),
            "vitamine_d": self._extract_nutrient(nutriments, "vitamin-d", "µg"),
            "vitamine_b1": self._extract_nutrient(nutriments, "vitamin-b1", "mg"),
            "vitamine_b2": self._extract_nutrient(nutriments, "vitamin-b2", "mg"),
            "vitamine_b3": self._extract_nutrient(nutriments, "vitamin-pp", "mg"),  # B3 is also known as PP
            "vitamine_b6": self._extract_nutrient(nutriments, "vitamin-b6", "mg"),
            "vitamine_b12": self._extract_nutrient(nutriments, "vitamin-b12", "µg"),
            "vitamine_e": self._extract_nutrient(nutriments, "vitamin-e", "mg"),
            "vitamine_k": self._extract_nutrient(nutriments, "vitamin-k", "µg"),
            "omega_3": self._extract_nutrient(nutriments, "omega-3-fat", "g"),
            "omega_6": self._extract_nutrient(nutriments, "omega-6-fat", "g"),
            "ingredients": product.get("ingredients_text", ""),
            "additifs": ", ".join(product.get("additives_tags", [])),
            "allergenes": ", ".join(product.get("allergens_tags", [])),
            "certifications": ", ".join(product.get("labels_tags", [])),
            "pays_origine": ", ".join(product.get("countries_tags", [])),
            "lieu_fabrication": product.get("manufacturing_places", ""),
            "instructions_conservation": product.get("conservation_conditions", ""),
            "mode_preparation": product.get("preparation", ""),
            "date_expiration": "",  # Not typically available in the API
            "code_barres": product.get("code", ""),
            "site_internet_marque": product.get("official_website", ""),
            "service_client_contact": product.get("contact", "")
        }
        
        return field_mapping.get(field_name, "")
    
    def _extract_volume(self, product):
        """Try to extract volume information from product data"""
        if "quantity" in product and "l" in product["quantity"].lower():
            return product["quantity"]
        return ""
    
    def scrape_product(self, barcode):
        """Scrape a single product by barcode"""
        try:
            url = f"{self.base_url}/{barcode}.json"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == 1:  # 1 means success
                    return data.get("product", {})
            return None
        except Exception as e:
            print(f"Error scraping product {barcode}: {e}")
            return None
    
    def search_products(self, page=1, page_size=50):
        """Search for products with the API"""
        try:
            url = f"https://world.openfoodfacts.org/api/v2/search"
            params = {
                "page": page,
                "page_size": page_size,
                "sort_by": "popularity_key",
                "fields": "code,product_name,brands_tags,categories_tags,packaging_tags,quantity,nutriments,ingredients_text,additives_tags,allergens_tags,labels_tags,countries_tags,manufacturing_places,conservation_conditions,preparation,official_website,contact"
            }
            
            response = requests.get(url, headers=self.headers, params=params, timeout=15)
            
            if response.status_code == 200:
                data = response.json()
                return data.get("products", [])
            return []
        except Exception as e:
            print(f"Error searching products on page {page}: {e}")
            return []
    
    def process_product(self, product):
        """Process a product and extract all required fields"""
        product_data = {}
        for field in self.fields:
            product_data[field] = self._get_field_value(product, field)
        
        return product_data
    
    def save_to_csv(self):
        """Save collected products to CSV file"""
        if not self.products:
            print("No products to save!")
            return
            
        try:
            df = pd.DataFrame(self.products)
            df.to_csv(self.output_file, index=False, encoding='utf-8')
            print(f"Successfully saved {len(self.products)} products to {self.output_file}")
        except Exception as e:
            print(f"Error saving to CSV: {e}")
            
            # Backup save attempt using csv module
            try:
                with open(self.output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=self.fields)
                    writer.writeheader()
                    writer.writerows(self.products)
                print(f"Backup save successful: {len(self.products)} products saved to {self.output_file}")
            except Exception as e2:
                print(f"Backup save also failed: {e2}")
    
    def run(self):
        """Run the scraper to collect the target number of products"""
        page = 1
        page_size = 100  # Maximum allowed by the API
        
        print(f"Starting to scrape {self.target_count} food products...")
        
        progress_bar = tqdm(total=self.target_count, desc="Scraping products")
        
        try:
            while len(self.products) < self.target_count:
                print(f"Fetching page {page}...")
                products_batch = self.search_products(page, page_size)
                
                if not products_batch:
                    print(f"No more products found or reached API limit. Stopping at {len(self.products)} products.")
                    break
                
                for product in products_batch:
                    if len(self.products) >= self.target_count:
                        break
                    
                    processed_product = self.process_product(product)
                    if processed_product:
                        self.products.append(processed_product)
                        progress_bar.update(1)
                
                page += 1
                
                # Be nice to the API server
                time.sleep(1 + random.random())
                
                # Save intermediate results every 500 products
                if len(self.products) % 500 == 0:
                    print(f"Saving intermediate results ({len(self.products)} products)...")
                    self.save_to_csv()
                
        except KeyboardInterrupt:
            print("\nScraping interrupted by user.")
        except Exception as e:
            print(f"Error during scraping: {e}")
        finally:
            progress_bar.close()
            self.save_to_csv()
            print(f"Scraping completed. Total products collected: {len(self.products)}")

def main():
    output_file = "food_data.csv"
    target_count = 2000
    
    scraper = FoodScraper(target_count=target_count, output_file=output_file)
    scraper.run()

if __name__ == "__main__":
    main()
