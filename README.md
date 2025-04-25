# Food Data Scraper

A Python script for scraping food product data from the Open Food Facts database and saving it to a CSV file with comprehensive nutritional information.

## Features

- Scrapes up to 2000 food products from Open Food Facts database
- Extracts detailed nutritional information and product details
- Saves data in a well-structured CSV format
- Includes proper API rate limiting to avoid server overload
- Shows progress bar during scraping
- Performs intermediate saves to prevent data loss

## Requirements

- Python 3.7+
- Required packages: requests, beautifulsoup4, pandas, tqdm

## Installation

1. Clone or download this repository
2. Install the required packages:

```
pip install -r requirements.txt
```

## Usage

Run the script with:

```
python main.py
```

The script will:
1. Connect to the Open Food Facts API
2. Retrieve food product data
3. Extract all required nutritional and product information
4. Save the data to `food_data.csv` in the same directory

## Data Fields

The script collects the following information for each product:

- `id_produit`: Unique identifier for the product
- `nom_produit`: Product name
- `marque`: Brand name
- `categorie`: Product category
- `sous_categorie`: Product subcategory
- `type_emballage`: Packaging type
- `poids_net`: Net weight (e.g., "250g")
- `volume`: Volume (e.g., "1L")
- Nutritional information:
  - `energie_kcal`: Energy in kcal
  - `energie_kj`: Energy in kJ
  - `lipides`: Fat content
  - `acides_gras_satures`: Saturated fat
  - `acides_gras_mono_insatures`: Monounsaturated fat
  - `acides_gras_poly_insatures`: Polyunsaturated fat
  - `cholesterol`: Cholesterol
  - `glucides`: Carbohydrates
  - `sucres`: Sugars
  - `amidon`: Starch
  - `fibres_alimentaires`: Dietary fiber
  - `proteines`: Protein
  - `sel`: Salt
  - `sodium`: Sodium
  - Various vitamins and minerals
  - `omega_3` and `omega_6` content
- Product details:
  - `ingredients`: Ingredient list
  - `additifs`: Additives
  - `allergenes`: Allergens
  - `certifications`: Certifications (e.g., "Bio, Halal")
  - `pays_origine`: Country of origin
  - `lieu_fabrication`: Manufacturing location
  - `instructions_conservation`: Storage instructions
  - `mode_preparation`: Preparation instructions
  - `date_expiration`: Expiration date
  - `code_barres`: Barcode
  - `site_internet_marque`: Brand's website
  - `service_client_contact`: Customer service contact

## Notes

- The script respects the Open Food Facts API by implementing rate limiting
- Some products may have incomplete information
- The script handles API errors gracefully and continues scraping
- You can modify the target number of products in the main() function
