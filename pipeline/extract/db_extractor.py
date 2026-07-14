import psycopg2
import pandas as pd


class DatabaseLoader:
    def __init__(self, host, port, database, user, password):
        self.connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=database,
            user=user,
            password=password,
        )

    def load_customers(self) -> pd.DataFrame:
        return pd.read_sql(
            "SELECT * FROM customers",
            self.connection,
        )

    def load_products(self) -> pd.DataFrame:
        return pd.read_sql(
            "SELECT * FROM products",
            self.connection,
        )

    def close(self):
        self.connection.close()
    

db = DatabaseLoader(
    host="localhost",
    port=5433,
    database="ecommerce_db",
    user="myuser",
    password="mypassword"
)

# customers_df = db.load_customers()
# products_df = db.load_products()

# print(customers_df.head())
# print(products_df.head())





