import pandas as pd
import os

# enter csv file name
tiktok_file = "Shipped order-2025-10-06-15_15.csv"
product_file = "productList.csv"

# if product list csv doesnt exist, create it
if not os.path.exists(product_file):
    print("Product list not found. Creating a new one...")
    product_data = pd.DataFrame(columns = ["Seller SKU", "Variation", "Quantity Used", "Product SKU", 
                                       "Product SKU 2", "Product SKU 3", "Product SKU 4",
                                       "Product SKU 5", "Product SKU 6", "Product SKU 7"])
else:
    # check if product list csv file has all columns
    product_data = pd.read_csv(product_file)
    needed_cols = ["Seller SKU", "Variation", "Quantity Used", "Product SKU", 
                   "Product SKU 2", "Product SKU 3", "Product SKU 4",
                   "Product SKU 5", "Product SKU 6", "Product SKU 7"]

    missing = [col for col in needed_cols if col not in product_data.columns]

# open csv files
tiktok_data = pd.read_csv(tiktok_file)


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
    new_items[["Quantity Used", "Product SKU", "Product SKU 2", "Product SKU 3", 
               "Product SKU 4", "Product SKU 5", "Product SKU 6", 
               "Product SKU 7"]] = "N/A"
    
    new_items = new_items[["Seller SKU", "Variation", "Quantity Used", "Product SKU", 
                           "Product SKU 2","Product SKU 3", 
                           "Product SKU 4", "Product SKU 5", "Product SKU 6", 
                           "Product SKU 7"]]

    updated_product_data = pd.concat([product_data.drop(columns = ["key"]), new_items], ignore_index = True)
    updated_product_data.to_csv(product_file, index = False)
    