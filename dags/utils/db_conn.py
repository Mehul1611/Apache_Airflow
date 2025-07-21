from airflow.providers.postgres.hooks.postgres import PostgresHook
import psycopg2
import logging

def get_pg_hook():
    try:
        hook = PostgresHook(postgres_conn_id="POSTGRES_CONN")
        print("✅ Successfully initialized PostgresHook for 'POSTGRES_CONN'")
        return hook
    except Exception as e:
        print(f"❌ Failed to initialize PostgresHook: {e}")
        raise

# def get_db_conn():
#     conn = psycopg2.connect(
#     dbname="airflow",
#     user="airflow",
#     password="airflow",
#     host="localhost", 
#     port=5433
# )
#     return conn