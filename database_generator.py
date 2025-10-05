import pandas as pd
import os

# enter csv file name
tiktok_file = "Shipped order-2025-10-02-22_07.csv"
product_file = "productList.csv"

# if product list csv doesnt exist, create it
if not os.path.exists(product_file):
    print("Product list not found. Creating a new one...")
    empty_db = pd.DataFrame(columns = ["Seller SKU", "Variation", "Product SKU", 
                                       "Product SKU 2", "Quantity Used"])
    empty_db.to_csv(product_file, index = False)

# open csv files
tiktok_data = pd.read_csv(tiktok_file)
product_data = pd.read_csv(product_file)

# creating composite keys
tiktok_data["key"] = tiktok_data["Seller SKU"].astype(str).str.strip() + "_" + tiktok_data["Variation"].astype(str).str.strip()
product_data["key"] = product_data["Seller SKU"].astype(str).str.strip() + "_" + product_data["Variation"].astype(str).str.strip()

# find rows in tiktok data that are not in product data
new_items = tiktok_data[~tiktok_data["key"].isin(product_data["key"])].copy()

# remove duplicates
new_items = new_items.drop_duplicates(subset = ["key"])

# add new items
if new_items.empty:
    print("All TikTok items already exist in the database!!")
else:
    print(f"Found {len(new_items)} new items not in database:\n")
    print(new_items[["Seller SKU", "Variation"]].to_string(index = False))

    # add to product list
    new_items["Product SKU"] = "PLS UPDATE"
    new_items["Product SKU 2"] = "PLS UPDATE"
    new_items["Quantity Used"] = "PLS UPDATE"
    new_items = new_items[["Seller SKU", "Variation", "Product SKU", "Product SKU 2", "Quantity Used"]]

    updated_product_data = pd.concat([product_data.drop(columns = ["key"]), new_items], ignore_index = True)
    updated_product_data.to_csv(product_file, index = False)
    