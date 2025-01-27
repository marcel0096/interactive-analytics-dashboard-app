import pandas as pd

########################################################################################
#################################### Load datasets #####################################
########################################################################################

customers = pd.read_csv("data/customers.csv")
orders = pd.read_csv("data/orders.csv")
sales = pd.read_csv("data/sales.csv")
products = pd.read_csv("data/products.csv")


########################################################################################
############################# Analyze & sanitize datasets ##############################
########################################################################################


# This is used to get an overview of the data and see whether there are N/A values or duplicates
def summarize_data(df, name):
    print(f"--- {name} Summary ---")
    print("Shape:", df.shape)
    print("Data Types:\n", df.dtypes)
    print("Columns:", df.columns.tolist())
    print("Missing Values:\n", df.isna().sum())
    print("\nDuplicate Values in Columns:")
    for col in df.columns:
        num_duplicates = df[col].duplicated().sum()
        print(f"{col}: {num_duplicates} duplicate(s)")
    print("Sample Data:\n", df.head(), "\n")
    print("-" * 50)


# Uncomment to see the summary of each dataset
# summarize_data(customers, "Customers")
# summarize_data(orders, "Orders")
# summarize_data(sales, "Sales")
# summarize_data(products, "Products")

# Products table has duplicates of Product.ID, which is the primary key and should be unique
# Thus only keeping the first occurrence of each Product.ID
# Remove duplicates, keeping the first occurrence for each Product.ID
products = products.drop_duplicates(subset="Product.ID", keep="first")

# Format the order date to pd datetime
orders["Order.Date"] = pd.to_datetime(orders["Order.Date"])


########################################################################################
################################### Merge datasets #####################################
########################################################################################

merged_data = pd.merge(orders, sales, on="Order.ID")
merged_data = pd.merge(merged_data, products, on="Product.ID")
# This merge step drops customers that have not placed any orders yet,
# since they are not relevant for sales analysis
merged_data = pd.merge(merged_data, customers, on="Customer.ID")
