from extract.file_extractor import EventLoader
from extract.db_extractor import DatabaseLoader
from transform.transformer import DataTransformer
from load.loader import Loader


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

        events_df = event_loader.load()

        products_df = db.load_products()
        customers_df = db.load_customers()

        transformer = DataTransformer(events_df,
        products_df,
        customers_df)

        report_df = transformer.transform()

        loader = Loader("reports/sales_report.csv")
        loader.save(report_df)


if __name__ == "__main__":
    Pipeline().run()