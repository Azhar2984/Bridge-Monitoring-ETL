from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_timestamp, to_date

spark = SparkSession.builder \
    .appName("BronzeLayerIngest") \
    .master("local[*]") \
    .getOrCreate()

# Landing directories for incoming sensor data
sensor_sources = {
    "temperature": "streams/bridge_temperature",
    "vibration": "streams/bridge_vibration",
    "tilt": "streams/bridge_tilt"
}

bronze_dir = "bronze"

for sensor_name, source_path in sensor_sources.items():
    stream_df = spark.readStream.json(source_path)
    
    # parse timestamps and add processing columns
    processed_df = stream_df.withColumn("event_time_ts", col("event_time").cast("timestamp")) \
                            .withColumn("ingest_time_ts", current_timestamp()) \
                            .withColumn("partition_date", to_date(col("event_time_ts")))

    # write to bronze layer with checkpointing
    processed_df.writeStream \
        .format("parquet") \
        .option("path", f"{bronze_dir}/{sensor_name}") \
        .option("checkpointLocation", f"checkpoints/bronze_{sensor_name}") \
        .start()

spark.streams.awaitAnyTermination()
