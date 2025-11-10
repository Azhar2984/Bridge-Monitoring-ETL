# Bridge Monitoring using PySpark

This project simulates IoT bridge sensors and builds a real-time ETL pipeline using PySpark Structured Streaming.

## Folder Structure

bridge-monitoring/
├── data_generator/          → Generates fake bridge sensor data  
├── pipelines/               → Bronze, Silver, Gold ETL scripts  
├── notebooks/               → Demo notebook  
├── metadata/                → Bridge metadata file  
└── checkpoints/             → Spark checkpoints

## Requirements

Python 3.8+  
PySpark 3.x  
Pandas, Matplotlib, Seaborn  
Jupyter Notebook  

## How to Run

1️⃣ Start Data Generator  

```bash
python data_generator/data_generator.py

Run ETL Pipelines
```bash
python pipelines/bronze_ingest.py
python pipelines/silver_enrichment.py
python pipelines/gold_aggregation.py


3️⃣ View Results
```bash
jupyter notebook notebooks/demo.ipynb
