import pandas as pd
import os

# enter csv file name
tiktok_file = "Shipped order-2025-10-02-22_07.csv"
product_file = "productListUpdated - Copy.csv"

# if product list csv doesnt exist, create it
if not os.path.exists(product_file):
    print("Product list not found. Creating a new one...")
    product_data = pd.DataFrame(columns=["Seller SKU", "Variation", "Quantity Used", "Product SKU", 
                                       "Product SKU 2", "Product SKU 3", "Product SKU 4",
                                       "Product SKU 5", "Product SKU 6", "Product SKU 7"])
else:
    # check if product list csv file has all columns
    product_data = pd.read_csv(product_file, keep_default_na=False)
    needed_cols = ["Seller SKU", "Variation", "Quantity Used", "Product SKU", 
                   "Product SKU 2", "Product SKU 3", "Product SKU 4",
                   "Product SKU 5", "Product SKU 6", "Product SKU 7"]

    # find missing values
    missing_cols = [col for col in needed_cols if col not in product_data.columns]

    # add missing values
    if missing_cols:
        for col in missing_cols:
            product_data[col] = "N/A"

        # reorganize columns if they aren't in speciified order    
        product_data = product_data[needed_cols]
        print(f"Added missing columns: {missing_cols} and set value to N/A")
    else:
        print("All required columns already exist!!")

# open csv files
tiktok_data = pd.read_csv(tiktok_file)

# creating composite keys
tiktok_data["key"] = tiktok_data["Seller SKU"].astype(str).str.strip() + "_" + tiktok_data["Variation"].astype(str).str.strip()
product_data["key"] = product_data["Seller SKU"].astype(str).str.strip() + "_" + product_data["Variation"].astype(str).str.strip()

# find rows in tiktok data that are not in product data
new_items = tiktok_data[~tiktok_data["key"].isin(product_data["key"])].copy()

# remove duplicates
new_items = new_items.drop_duplicates(subset=["key"])

# add new items
if new_items.empty:
    print("All TikTok items already exist in the database!!")
    
    # update product list if missing columns were added
    if missing_cols:
        product_data = product_data.drop(columns=["key"])
        product_data.to_csv(product_file, index=False)
else:
    print(f"Found {len(new_items)} new items not in database:\n")
    print(new_items[["Seller SKU", "Variation"]].to_string(index=False))

    # add to product list
    new_items[["Quantity Used", "Product SKU", "Product SKU 2", "Product SKU 3", 
               "Product SKU 4", "Product SKU 5", "Product SKU 6", 
               "Product SKU 7"]] = "N/A"
    
    new_items = new_items[["Seller SKU", "Variation", "Quantity Used", "Product SKU", 
                           "Product SKU 2","Product SKU 3", 
                           "Product SKU 4", "Product SKU 5", "Product SKU 6", 
                           "Product SKU 7"]]

    updated_product_data = pd.concat([product_data.drop(columns=["key"]), new_items], ignore_index=True)
    updated_product_data.to_csv(product_file, index=False)
    