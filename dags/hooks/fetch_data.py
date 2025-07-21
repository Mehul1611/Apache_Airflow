from datetime import datetime
from utils.db_conn import get_pg_hook

class Hooks:
    def __init__(self):
        self.conn = get_pg_hook()

    def create_tables(self):
        source_stmt = """
        CREATE TABLE IF NOT EXISTS fetch_data (
            id SERIAL PRIMARY KEY,
            name TEXT,
            age INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        target_stmt = """
        CREATE TABLE IF NOT EXISTS update_data (
            id SERIAL PRIMARY KEY,
            name TEXT,
            age INT,
            time_updated TIMESTAMP
        );
        """

        try:
            with self.conn.get_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(source_stmt)
                    cursor.execute(target_stmt)
                conn.commit()
            print("Tables created or already exist.")
        except Exception as e:
            print(f"Table creation failed: {e}")

    def extract_data(self):
        try:
            query = "SELECT * FROM fetch_data;"
            df = self.conn.get_pandas_df(query)
            print("Data extracted:")
            print(df)
            return df
        except Exception as e:
            print(f" Data extraction failed: {e}")
            return None

    def transform_data(self, df):
        if df is not None:
            df['time_updated'] = datetime.now()
            print("Data transformed.")
            return df
        else:
            print("No data to transform.")
            return None

    def load_data(self, df):
        if df is None:
            print( "No data to load.")
            return

        try:
            print(f'The extracted data frame: {df}')
            col = list(df.columns)
            rows = list(df.itertuples(index=False, name=None))
            
            self.conn.insert_rows(
                table="update_data",
                rows=rows,
                target_fields=col,
                replace=False
            )
            print("Data inserted into update_data.")

            with self.conn.get_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("CALL sp_update();")
                conn.commit()
            print("Stored procedure `sp_update()` called.")
        except Exception as e:
            print(f"Data load failed: {e}")

    def run_etl_pipeline(self):
        self.create_tables()
        df = self.extract_data()
        df = self.transform_data(df)
        self.load_data(df)
