import pandas as pd
import os

# csv files
tiktok_file = "Shipped order-2025-10-02-22_07.csv"
product_file = "productListUpdated.csv"
monthly_report_file = "monthlyBarcodeReport.csv"

# open csv files
tiktok_data = pd.read_csv(tiktok_file)
product_db = pd.read_csv(product_file)

if not os.path.exists(monthly_report_file):
    print("Monthly Barcode Report not found!, Creating file...")
    empty_db = pd.DataFrame(columns = ["Product SKU", "Quantity"])
    empty_db.to_csv(monthly_report_file, index = False)

monthly_barcodes = pd.read_csv(monthly_report_file)


# read TikTok order data and quantify the amount of each barcode used
print(tiktok_data.columns)