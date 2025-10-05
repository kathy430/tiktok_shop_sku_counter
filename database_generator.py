import pandas as pd

# enter csv file name
fileName = "Shipped order-2025-10-02-22_07.csv"

# open csv file
data = pd.read_csv(fileName)


print(data.head())