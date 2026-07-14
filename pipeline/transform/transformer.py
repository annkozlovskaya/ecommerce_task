import pandas as pd


class DataTransformer:
    def __init__(
        self,
        events_df: pd.DataFrame,
        products_df: pd.DataFrame,
        customers_df: pd.DataFrame,
    ):
        self.events = events_df
        self.products = products_df
        self.customers = customers_df

    def transform(self) -> pd.DataFrame:
        # 1 Filter the events DataFrame to get only purchase events.
        purchases = self.events[self.events["event_type"] == "purchase"]

        # 2 Join the purchase events with the products DataFrame on product_id.
        purchases = purchases.merge(
            self.products,
            on="product_id",
            how="left",
        )


        # 3 Join the result with the customers DataFrame on customer_id.
        purchases = purchases.merge(
            self.customers,
            on="customer_id",
            how="left",
        )

        # 4. Create a new column total_revenue = quantity * price.
        purchases["total_revenue"] = (
            purchases["quantity"] * purchases["price"]
        )

        # 5. Aggregate: groupby() the DataFrame by category and customer segment.
        # Calculate the sum of total_revenue, sum of quantity (as units_sold), and the nunique (count distinct) of customer_id.
        result = (
            purchases
            .groupby(
                ["category", "segment"],
                as_index=False,
            )
            .agg(
                total_revenue=("total_revenue", "sum"),
                units_sold=("quantity", "sum"),
                unique_customers=("customer_id", "nunique"),
            )
        )

        return result
    

