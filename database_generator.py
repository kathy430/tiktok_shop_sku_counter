import pandas as pd
import os
import sys

# enter csv file name
tiktok_file = "Shipped order-2025-10-02-22_07.csv"
product_file = "productListTest.csv"

# open tiktok csv
tiktok_data = pd.read_csv(tiktok_file)

# if product list csv doesnt exist, create it
if not os.path.exists(product_file):
    print("Product list not found. Creating a new one...")
    product_data = pd.DataFrame(columns=["SKU ID", "Seller SKU", "Product Name", "Variation", "Quantity Used",
                                       "Product SKU", "Product SKU 2", "Product SKU 3", "Product SKU 4",
                                       "Product SKU 5", "Product SKU 6", "Product SKU 7"])
else:
    # check if product list csv file has all columns
    product_data = pd.read_csv(product_file, keep_default_na=False)
    needed_cols = ["SKU ID", "test column", "Seller SKU", "Product Name", "Variation", "Quantity Used",
                   "Product SKU", "Product SKU 2", "Product SKU 3", "Product SKU 4",
                   "Product SKU 5", "Product SKU 6", "Product SKU 7"]

    # find missing values
    missing_cols = [col for col in needed_cols if col not in product_data.columns]

    # add missing column and set to N/A
    if missing_cols:
        # exit with error if missing key column
        if "SKU ID" in missing_cols:
            print("Missing key column SKU ID!!", file=sys.stderr)
            sys.exit(1)

        for col in missing_cols:
            product_data[col] = "N/A"

        # reorganize columns if they aren't in speciified order    
        product_data = product_data[needed_cols]

        print(f"Added missing columns: {missing_cols} and set values to N/A")
    else:
        print("All required columns already exist!!")



# creating composite keys
#tiktok_data["key"] = tiktok_data["SKU ID"].astype(str).str.strip() + "_" + tiktok_data["Seller SKU"].astype(str).str.strip() + "_" + tiktok_data["Variation"].astype(str).str.strip()
#product_data["key"] = product_data["SKU ID"].astype(str).str.strip() + "_" + product_data["Product Name"].astype(str).str.strip() + "_" + product_data["Variation"].astype(str).str.strip()

# find rows in tiktok data that are not in product data
new_items = tiktok_data[~tiktok_data["SKU ID"].isin(product_data["SKU ID"])].copy()

# remove duplicates
new_items = new_items.drop_duplicates(subset=["SKU ID"])

# add new items
if new_items.empty:
    print("All TikTok items already exist in the database!!")
else:
    print(f"Found {len(new_items)} new items not in database:\n")
    print(new_items[["Seller SKU", "Product Name", "Variation"]].to_string(index=False))

    # add to product list
    new_items[["Quantity Used", "Product SKU", "Product SKU 2", "Product SKU 3", 
               "Product SKU 4", "Product SKU 5", "Product SKU 6", "Product SKU 7"]] = "N/A"
    
    # fill in Product SKU only if Seller SKU is a barcode
    def is_barcode(value):
        value = str(value).strip()
        return value.isdigit()
    
    new_items["Product SKU"] = new_items["Seller SKU"]
    
    new_items = new_items[["SKU ID", "Seller SKU", "Product Name", "Variation", "Quantity Used",
                           "Product SKU", "Product SKU 2","Product SKU 3", "Product SKU 4", 
                           "Product SKU 5", "Product SKU 6", "Product SKU 7"]]

    product_data = pd.concat([product_data, new_items], ignore_index=True)
    
# update product list if missing columns were added
if missing_cols:
    print(missing_cols)
    merged = 
    # fill out missing column information
    for col in missing_cols:
        if col == "test column":
            

    print("Writing missing columns to csv file...")
    
    
product_data.to_csv(product_file, index=False)
    