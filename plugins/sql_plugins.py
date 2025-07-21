# from airflow.plugins_manager import AirflowPlugin
# from airflow.models import Connection
# from airflow import settings
# import os


# def add_postgres_connection():
#     conn_id = "POSTGRES_CONN"
    
#     conn = Connection(
#         conn_id=conn_id,
#         conn_type="postgres",
#         host="test_db",
#         login= "test_user",
#         password= "test_pass",
#         schema= "test_db",
#         port= 5432,
#     )
#     session = settings.Session()
#     existing = session.query(Connection).filter(Connection.conn_id == conn_id).first()
#     if existing:
#         session.delete(existing)
#         session.commit()
#     session.add(conn)
#     session.commit()
#     print(f" PostgreSQL connection '{conn_id}' added.")
    

# class PostgresConnectionPlugin(AirflowPlugin):
#     name = "postgres_connection_plugin"

#     def on_load(self, *args, **kwargs):
#         add_postgres_connection()
