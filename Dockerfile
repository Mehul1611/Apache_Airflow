FROM apache/airflow:3.0.3
COPY requirements.txt ./
USER root
RUN apt-get update && apt-get install -y libleveldb-dev build-essential g++ git && apt-get clean
USER airflow

RUN pip install --upgrade apache-airflow-providers-amazon==8.0.0 \
    apache-airflow-providers-google \
    apache-airflow-providers-mysql \
    apache-airflow-providers-postgres

# RUN pip install -r requirements.txt --no-cache-dir
# RUN pip3 install plyvel