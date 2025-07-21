# # utils/connections.py
# from airflow.models.connection import Connection
# from airflow.utils.db import provide_session
# from airflow.settings import Session

# @provide_session
# def add_postgres_connection(session: Session = None):
#     conn_id = "POSTGRES_CONN"
#     existing = session.query(Connection).filter(Connection.conn_id == conn_id).first()
#     if existing:
#         session.delete(existing)
#         session.commit()
#     conn = Connection(
#         conn_id=conn_id,
#         conn_type="postgres",
#         host="test_db",
#         login="test_user",
#         password="test_pass",
#         schema="test_db",
#         port=5432,
#     )
#     session.add(conn)
#     session.commit()
#     print(f"Connection '{conn_id}' added.")

# from airflow.models import Connection
# from airflow.providers.postgres.hooks.postgres import PostgresHook
# from airflow import settings

# def ensure_postgres_connection():
#     conn_id = "my_postgres_conn"
#     session = settings.Session()

#     existing_conn = session.query(Connection).filter(Connection.conn_id == conn_id).first()
#     if existing_conn:
#         print(f"Connection '{conn_id}' already exists.")
#     else:
#         new_conn = Connection(
#             conn_id=conn_id,
#             conn_type="postgres",
#             host="test_db",
#             schema="test_user",
#             login="test_pass",
#             password="test_db",
#             port=5432,
#         )
#         session.add(new_conn)
#         session.commit()
#         print(f"Connection '{conn_id}' created.")

# def use_postgres_connection():
#     hook = PostgresHook(postgres_conn_id="my_postgres_conn")
#     with hook.get_conn() as conn:
#         with conn.cursor() as cur:
#             cur.execute("SELECT 1;")
#             result = cur.fetchone()
#             print(f"Result of test query: {result}")
