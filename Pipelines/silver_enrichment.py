from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import os

spark = SparkSession.builder.appName("SilverEnrichment").master("local[*]").getOrCreate()

# Load static metadata
metadata_path = "metadata/bridges.csv"

if os.path.exists(metadata_path) and os.path.getsize(metadata_path) > 0:
    bridges = spark.read.csv(metadata_path, header=True, inferSchema=True)
    metadata_available = True
else:
    print("Warning: metadata/bridges.csv is empty or missing. Stream will continue without enrichment.")
    bridges = None
    metadata_available = False

sensors = ["temperature", "vibration", "tilt"]
silver_path = "silver"

for sensor in sensors:
    df = spark.readStream.parquet(f"bronze/{sensor}")

    # join with metadata only if available
    if metadata_available:
        df = df.join(bridges, df.bridge_id == bridges.bridge_id, how="left")

    # data quality checks
    if sensor == "temperature":
        df = df.filter((col("value").between(-40, 80)))
    elif sensor == "vibration":
        df = df.filter(col("value") >= 0)
    else:  # tilt
        df = df.filter(col("value").between(0, 90))

    query = df.writeStream \
        .format("parquet") \
        .option("path", f"{silver_path}/{sensor}") \
        .option("checkpointLocation", f"checkpoints/silver_{sensor}") \
        .start()

spark.streams.awaitAnyTermination()
