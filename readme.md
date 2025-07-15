# Apache Airflow Setup

### 1. Create Virtual Environment
```bash
python3 -m venv ~/Desktop/Airflow/airflow_env
source ~/Desktop/Airflow/airflow_env/bin/activate
```

---

### 2. Install Airflow (with constraints)
```bash
pip install --upgrade pip setuptools wheel

AIRFLOW_VERSION=2.8.1
PYTHON_VERSION=3.11
CONSTRAINT_URL="https://raw.githubusercontent.com/apache/airflow/constraints-${AIRFLOW_VERSION}/constraints-${PYTHON_VERSION}.txt"

pip install "apache-airflow==${AIRFLOW_VERSION}" --constraint "${CONSTRAINT_URL}"
```

---


### 3. Set AIRFLOW_HOME

```bash
export AIRFLOW_HOME=~/Desktop/Airflow
mkdir -p "$AIRFLOW_HOME"
```

- To make this setting permanent in your system run the below command:
```bash
echo 'export AIRFLOW_HOME=~/Desktop/Airflow' >> ~/.zshrc
source ~/.zshrc
```

---

### 4. Initialize Airflow
```bash 
airflow db init
```

---
---

# Start Airflow Service
### 1. Start Webserver

```bash
airflow webserver --port 8080
```
### 2. Start Scheduler (In a new tab)

```bash 
airflow scheduler
```