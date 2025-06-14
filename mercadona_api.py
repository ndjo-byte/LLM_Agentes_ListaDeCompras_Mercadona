import requests 
import csv
import os



# API Call to get categories
categories_url = "https://tienda.mercadona.es/api/categories/"
response = requests.get(categories_url)
data = response.json()

# Drill down to get category names
category_map = {
    subcat['id']: subcat['name']
    for supercat in data['results']
    for subcat in supercat['categories']
}

# API Call to get products
def get_products():
    all_products = {}
    for category_id in category_map.keys():
        products_url = f"https://tienda.mercadona.es/api/categories/{category_id}/"
        response = requests.get(products_url) 
        data = response.json()
        all_products[category_id] = data

    return all_products


def show_simple_products():
    raw_data = get_products()

    print("DEBUG: raw_data type:", type(raw_data))
    print("DEBUG: raw_data keys:", raw_data.keys())

    for section_id, section_data in raw_data.items():
        categories = section_data.get('categories', [])
        print(f"Section {section_id} has {len(categories)} categories")

        for category in categories:
            print(f"  Category: {category.get('name')}")
            products = category.get('products', [])
            print(f"    -> Found {len(products)} products")

            for product in products:
                display_name = product.get('display_name')
                unit_price = product.get('price_instructions', {}).get('unit_price')
                unit_size = product.get('price_instructions', {}).get('unit_size')
                size_format = product.get('price_instructions', {}).get('size_format')
                print(f"      - {display_name}: {unit_price} € / {unit_size} {size_format}")

def save_simple_products():
    raw_data = get_products()
    simple_products = []
    


    for section_id, section_data in raw_data.items():
        categories = section_data.get('categories', [])
        print(f"Section {section_id} has {len(categories)} categories")

        for category in categories:
            print(f"  Category: {category.get('name')}")
            products = category.get('products', [])
            print(f"    -> Found {len(products)} products")

            for product in products:
                display_name = product.get('display_name')
                unit_price = product.get('price_instructions', {}).get('unit_price')
                unit_size = product.get('price_instructions', {}).get('unit_size')
                size_format = product.get('price_instructions', {}).get('size_format')
                simple_products.append({
                    'display_name': display_name,
                    'unit_price': unit_price,
                    'unit_size': unit_size,
                    'size_format': size_format
                })  

    with open('csv_files/simple_products.csv', 'w', newline='') as csvfile:
        fieldnames = ['display_name', 'unit_price', 'unit_size', 'size_format']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(simple_products)

if __name__ == "__main__":
    os.makedirs("csv_files", exist_ok=True)
    show_simple_products()



    








