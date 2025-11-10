**Bridge Monitoring using PySpark**

This project simulates IoT bridge sensors and builds a real-time data pipeline using PySpark Structured Streaming.
It follows the Bronze → Silver → Gold ETL design to collect, clean, and analyze sensor data like temperature, vibration, and tilt.

**Folder Structure**

bridge-monitoring/
│
├── data_generator/          → Generates fake bridge sensor data  
├── pipelines/               → Contains Bronze, Silver, and Gold ETL scripts  
├── notebooks/               → Jupyter notebook for demo and visualization  
├── metadata/                → Includes bridge metadata file  
└── checkpoints/             → Spark checkpoints (ignored in Git)

**Requirements**

Python 3.8 or higher

PySpark 3.x

Pandas, Matplotlib, Seaborn

Jupyter Notebook

**How to Run**

python data_generator/data_generator.py

**Run ETL Pipelines**

python pipelines/bronze_ingest.py
python pipelines/silver_enrichment.py
python pipelines/gold_aggregation.py

**View Results**

jupyter notebook notebooks/demo.ipynb


