from datetime import datetime
from utils.db_conn import get_pg_hook

class Hooks:
    def __init__(self):
        self.conn = get_pg_hook()

    def insert_data(self):
        try:
            with self.conn.get_conn() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DROP TABLE IF EXISTS fetch_data;")
                    cursor.execute("DROP TABLE IF EXISTS update_data;")

                    cursor.execute("""
                    CREATE TABLE fetch_data (
                        id SERIAL PRIMARY KEY,
                        name TEXT,
                        age INT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    );
                    """)

                    cursor.execute("""
                    INSERT INTO fetch_data (name, age) VALUES
                    ('Alice', 28),
                    ('Bob', 34),
                    ('Charlie', 22);
                    """)

                    cursor.execute("""
                    CREATE TABLE update_data (
                        id SERIAL PRIMARY KEY,
                        name TEXT,
                        age INT,
                        time_updated TIMESTAMP
                    );
                    """)

                conn.commit()
            print("Tables dropped, recreated, and dummy data inserted.")
        except Exception as e:
            print(f"Table setup failed: {e}")

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
            df = df.drop(columns=['created_at'])
            col = list(df.columns)
            rows = list(df.itertuples(index=False, name=None))
            
            self.conn.insert_rows(
                table="update_data",
                rows=rows,
                target_fields=col,
                replace=False
            )
            print("Data inserted into update_data.")
            query = "SELECT * FROM update_data;"
            new_df = self.conn.get_pandas_df(query)
            print(f"The new data frame {new_df}")
            
        except Exception as e:
            print(f"Data load failed: {e}")

    def run_etl_pipeline(self):
        self.insert_data()
        df = self.extract_data()
        df = self.transform_data(df)
        self.load_data(df)
