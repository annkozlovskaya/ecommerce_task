from extract.file_extractor import EventLoader
from extract.db_extractor import DatabaseLoader
from transform.transformer import DataTransformer
from load.loader import WorkWithFiles
import pandas as pd


class Pipeline:

    def run(self):

        event_loader = EventLoader("data")

        db = DatabaseLoader(
            host="localhost",
            port=5433,
            database="ecommerce_db",
            user="myuser",
            password="mypassword",
        )
        products_df = db.load_products()
        customers_df = db.load_customers()

        for zip_folder in event_loader.read_json():
            for json_data in zip_folder:
                events_df = pd.DataFrame(json_data)
                if "quantity" not in events_df.columns:
                    events_df["quantity"] = pd.NA
                try:
                    temp_df = pd.read_csv("reports/temp_sales_report.csv")
                except FileNotFoundError:
                    temp_df = pd.DataFrame()
                transformer = DataTransformer(events_df, 
                temp_df, 
                products_df,
                customers_df)

                report_df = transformer.transform()

                loader_template = WorkWithFiles("reports/temp_sales_report.csv")
                loader_template.save(report_df)
        
        report_df = transformer.last_aggregation(report_df)
        loader_result = WorkWithFiles("reports/sales_report_new.csv")
        loader_result.save(report_df)
        loader_template.delete("reports/temp_sales_report.csv")



if __name__ == "__main__":
    Pipeline().run()