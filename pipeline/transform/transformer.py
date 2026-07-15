import pandas as pd


class DataTransformer:
    def __init__(
        self,
        events_df: pd.DataFrame,
        temp_df: pd.DataFrame,
        products_df: pd.DataFrame,
        customers_df: pd.DataFrame,
    ):
        self.events = events_df
        self.temp_df = temp_df
        self.products = products_df
        self.customers = customers_df

    def transform(self) -> pd.DataFrame:
        purchases = self._filter_purchases()
        purchases = self._merge_products(purchases)
        purchases = self._merge_customers(purchases)
        purchases = self._calculate_revenue(purchases)
        purchases = self._aggregate_new(purchases)
        purchases = self._concat_temperary(purchases)
        return self._aggregate_all(purchases)
    
    def _filter_purchases(self) -> pd.DataFrame:
        # 1 Filter the events DataFrame to get only purchase events.
        return self.events[self.events["event_type"] == "purchase"]
        
    def _merge_products(self, df: pd.DataFrame) -> pd.DataFrame:
        # 2 Join the purchase events with the products DataFrame on product_id.
        return df.merge(
            self.products,
            on="product_id",
            how="left",
        )

        
    def _merge_customers(self, df: pd.DataFrame) -> pd.DataFrame:
        # 3 Join the result with the customers DataFrame on customer_id.
        return df.merge(
            self.customers,
            on="customer_id",
            how="left",
        )

    def _calculate_revenue(self, df: pd.DataFrame) -> pd.DataFrame:
        df["total_revenue"] = df["quantity"] * df["price"]
        return df
    
    def _aggregate_new(self, df: pd.DataFrame) -> pd.DataFrame:

        return (
            df.groupby(
                ["category", "segment"],
                as_index=False,
            )
            .agg(
                total_revenue=("total_revenue", "sum"),
                units_sold=("quantity", "sum"),
                unique_customers=("customer_id", lambda s: ",".join(map(str, s.dropna().unique()))),
            )
        )
    def _concat_temperary(self, df: pd.DataFrame) -> pd.DataFrame:
        return pd.concat(
            [df, self.temp_df],
            ignore_index=True,
        )
    def _aggregate_all(self, df: pd.DataFrame) -> pd.DataFrame:

        return (
            df.groupby(
                ["category", "segment"],
                as_index=False,
            )
            .agg(
                total_revenue=("total_revenue", "sum"),
                units_sold=("units_sold", "sum"),
                unique_customers=("unique_customers", lambda s: ",".join({
                                                                            customer
                                                                            for value in s.dropna()
                                                                            for customer in str(value).split(",")
                                                                            if customer
                                                                        })),
            )
            .round(2)
        )
    
    def last_aggregation(self, df: pd.DataFrame) -> pd.DataFrame:
       df["unique_customers"] = df["unique_customers"].apply(lambda s: len(s.split(",")))
       return df

