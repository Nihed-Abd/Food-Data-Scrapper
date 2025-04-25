#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import random
import os
from tqdm import tqdm

def generate_food_data(target_count=2000, output_file="food_data.csv"):
    """
    Generate synthetic food data and save to CSV.
    This is a standalone function that doesn't require API access.
    """
    # Food categories
    categories = [
        "Produits laitiers", "Viandes", "Poissons", "Fruits", "Légumes", 
        "Céréales", "Boissons", "Snacks", "Conserves", "Surgelés",
        "Pâtisseries", "Confiseries", "Pâtes", "Riz", "Huiles",
        "Sauces", "Épices", "Soupes", "Charcuterie", "Fromages"
    ]
    
    # Brands
    brands = [
        "Danone", "Nestlé", "Carrefour", "Lidl", "Auchan", 
        "Bonduelle", "Président", "Barilla", "Fleury Michon", "Bonne Maman",
        "Kellogg's", "Knorr", "Lu", "Maggi", "Panzani",
        "Heinz", "Coca-Cola", "Pepsi", "Evian", "Cristaline"
    ]
    
    # Subcategories
    subcategories = {
        "Produits laitiers": ["Yaourt", "Fromage", "Crème", "Beurre", "Lait"],
        "Viandes": ["Boeuf", "Poulet", "Porc", "Agneau", "Charcuterie"],
        "Poissons": ["Saumon", "Thon", "Sardine", "Truite", "Fruits de mer"],
        "Fruits": ["Pomme", "Banane", "Orange", "Fraise", "Raisin"],
        "Légumes": ["Carotte", "Tomate", "Pomme de terre", "Salade", "Oignon"],
        "Céréales": ["Blé", "Avoine", "Maïs", "Riz", "Quinoa"],
        "Boissons": ["Eau", "Jus", "Soda", "Thé", "Café"],
        "Snacks": ["Chips", "Biscuits", "Crackers", "Barres", "Noix"],
        "Conserves": ["Légumes", "Fruits", "Poisson", "Viande", "Soupe"],
        "Surgelés": ["Pizza", "Légumes", "Plats préparés", "Glaces", "Viandes"]
    }
    
    # Packaging types
    packaging_types = [
        "Bouteille plastique", "Bouteille verre", "Boîte carton", 
        "Sachet plastique", "Barquette", "Pot en verre", "Conserve", 
        "Boîte métallique", "Film plastique", "Barquette sous vide"
    ]
    
    # Base nutrition values to randomize from
    base_nutrients = {
        "energie_kcal": (50, 600, " kcal"),
        "energie_kj": (200, 2500, " kJ"),
        "lipides": (0, 40, "g"),
        "acides_gras_satures": (0, 20, "g"),
        "acides_gras_mono_insatures": (0, 15, "g"),
        "acides_gras_poly_insatures": (0, 10, "g"),
        "cholesterol": (0, 100, "mg"),
        "glucides": (0, 80, "g"),
        "sucres": (0, 40, "g"),
        "amidon": (0, 30, "g"),
        "fibres_alimentaires": (0, 15, "g"),
        "proteines": (0, 30, "g"),
        "sel": (0, 5, "g"),
        "sodium": (0, 1000, "mg"),
        "calcium": (0, 500, "mg"),
        "fer": (0, 15, "mg"),
        "magnesium": (0, 100, "mg"),
        "zinc": (0, 5, "mg"),
        "vitamine_a": (0, 1000, "µg"),
        "vitamine_c": (0, 100, "mg"),
        "vitamine_d": (0, 15, "µg"),
        "vitamine_b1": (0, 2, "mg"),
        "vitamine_b2": (0, 2, "mg"),
        "vitamine_b3": (0, 20, "mg"),
        "vitamine_b6": (0, 2, "mg"),
        "vitamine_b12": (0, 5, "µg"),
        "vitamine_e": (0, 15, "mg"),
        "vitamine_k": (0, 80, "µg"),
        "omega_3": (0, 3, "g"),
        "omega_6": (0, 10, "g")
    }
    
    # Common allergens
    allergens = ["Gluten", "Lait", "Œufs", "Fruits à coque", "Soja", "Sésame", 
                "Crustacés", "Poisson", "Arachide", "Moutarde", "Céleri", "Lupin"]
    
    # Certifications
    certifications = ["Bio", "Label Rouge", "AOP", "IGP", "Commerce équitable", 
                     "Sans gluten", "Végan", "Halal", "Kasher", "AB"]
    
    # Conservation instructions
    conservation_instructions = [
        "À conserver au réfrigérateur entre 0°C et 4°C",
        "À conserver dans un endroit frais et sec",
        "À conserver à température ambiante",
        "À conserver à l'abri de la lumière et de l'humidité",
        "À conserver au congélateur à -18°C"
    ]
    
    # Preparation instructions
    preparation_instructions = [
        "Prêt à consommer",
        "À réchauffer 3 minutes au micro-ondes",
        "À cuire 10 minutes à la poêle",
        "À cuire 20 minutes au four à 180°C",
        "À décongeler avant consommation",
        "À diluer dans de l'eau",
        "Cuire à l'eau bouillante pendant 10 minutes"
    ]
    
    # Countries
    countries = ["France", "Italie", "Espagne", "Allemagne", "Belgique", 
                "Pays-Bas", "Suisse", "Royaume-Uni", "Portugal", "Grèce"]
    
    # Additives
    additives_list = ["E100", "E101", "E102", "E104", "E110", "E120", 
                     "E150", "E160", "E200", "E202", "E211", "E300", 
                     "E306", "E330", "E415", "E440", "E471", "E500"]
    
    # Fields for the CSV
    fields = [
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
    
    print(f"Generating {target_count} food products...")
    
    # Prepare products list
    products = []
    
    # Generate the products
    for i in tqdm(range(target_count), desc="Generating food data"):
        product_id = str(1000 + i)
        category = random.choice(categories)
        subcategory_options = subcategories.get(category, ["Standard"])
        subcategory = random.choice(subcategory_options)
        brand = random.choice(brands)
        
        # Generate a product name
        name_components = [
            f"{brand} {subcategory.lower()}",
            f"{brand} {subcategory.lower()} premium",
            f"{subcategory} {brand} tradition",
            f"{brand} - {subcategory} spécial",
            f"Le {subcategory.lower()} {brand}"
        ]
        product_name = random.choice(name_components)
        
        # Generate weight or volume
        has_weight = random.random() > 0.3
        has_volume = random.random() > 0.7
        weight = f"{random.randint(50, 2000)}g" if has_weight else ""
        volume = f"{random.randint(1, 5)}.{random.randint(0, 9)}L" if has_volume and not has_weight else ""
        
        # Number of ingredients
        num_ingredients = random.randint(3, 15)
        ingredients = []
        for _ in range(num_ingredients):
            ing = f"Ingrédient{random.randint(1, 50)}"
            percentage = round(random.uniform(1, 50), 1)
            ingredients.append(f"{ing} ({percentage}%)")
        ingredients_text = ", ".join(ingredients)
        
        # Generate random additives
        num_additives = random.randint(0, 5)
        product_additives = []
        for _ in range(num_additives):
            product_additives.append(random.choice(additives_list))
        additives_text = ", ".join(product_additives) if product_additives else ""
        
        # Generate random allergens
        num_allergens = random.randint(0, 3)
        product_allergens = []
        for _ in range(num_allergens):
            product_allergens.append(random.choice(allergens))
        allergens_text = ", ".join(product_allergens) if product_allergens else ""
        
        # Generate random certifications
        num_certifications = random.randint(0, 2)
        product_certifications = []
        for _ in range(num_certifications):
            product_certifications.append(random.choice(certifications))
        certifications_text = ", ".join(product_certifications) if product_certifications else ""
        
        # Base product data
        product = {
            "id_produit": product_id,
            "nom_produit": product_name,
            "marque": brand,
            "categorie": category,
            "sous_categorie": subcategory,
            "type_emballage": random.choice(packaging_types),
            "poids_net": weight,
            "volume": volume,
            "ingredients": ingredients_text,
            "additifs": additives_text,
            "allergenes": allergens_text,
            "certifications": certifications_text,
            "pays_origine": random.choice(countries),
            "lieu_fabrication": random.choice(countries),
            "instructions_conservation": random.choice(conservation_instructions),
            "mode_preparation": random.choice(preparation_instructions),
            "date_expiration": f"{random.randint(1, 30)}/{random.randint(1, 12)}/2025",
            "code_barres": f"{random.randint(1000000000000, 9999999999999)}",
            "site_internet_marque": f"www.{brand.lower().replace(' ', '')}.com",
            "service_client_contact": f"contact@{brand.lower().replace(' ', '')}.com"
        }
        
        # Add nutritional values
        for nutrient, (min_val, max_val, unit) in base_nutrients.items():
            if random.random() > 0.2:  # 80% chance to have this nutrient
                value = round(random.uniform(min_val, max_val), 1)
                product[nutrient] = f"{value}{unit}"
            else:
                product[nutrient] = ""
        
        products.append(product)
    
    # Save to CSV file
    try:
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(products)
        print(f"Successfully saved {len(products)} products to {output_file}")
        return True
    except Exception as e:
        print(f"Error saving to CSV: {e}")
        return False

if __name__ == "__main__":
    generate_food_data(2000, "food_data.csv")
