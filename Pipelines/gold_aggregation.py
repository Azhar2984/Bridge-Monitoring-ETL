from pyspark.sql import SparkSession
from pyspark.sql.functions import window, avg, max

spark = SparkSession.builder \
    .appName("GoldLayerAggregation") \
    .master("local[*]") \
    .getOrCreate()

silver_dir = "silver"
gold_dir = "gold"

# Temperature aggregation
temperature_stream = spark.readStream.parquet(f"{silver_dir}/temperature") \
    .withWatermark("event_time_ts", "2 minutes") \
    .groupBy("bridge_id", window("event_time_ts", "1 minute")) \
    .agg(avg("value").alias("avg_temperature"))

# Vibration aggregation
vibration_stream = spark.readStream.parquet(f"{silver_dir}/vibration") \
    .withWatermark("event_time_ts", "2 minutes") \
    .groupBy("bridge_id", window("event_time_ts", "1 minute")) \
    .agg(max("value").alias("max_vibration"))

# Tilt aggregation
tilt_stream = spark.readStream.parquet(f"{silver_dir}/tilt") \
    .withWatermark("event_time_ts", "2 minutes") \
    .groupBy("bridge_id", window("event_time_ts", "1 minute")) \
    .agg(max("value").alias("max_tilt_angle"))

# Join aggregated streams
bridge_metrics = temperature_stream.join(vibration_stream, ["bridge_id", "window"]) \
                                  .join(tilt_stream, ["bridge_id", "window"]) \
                                  .select("bridge_id", "window.start", "window.end", 
                                          "avg_temperature", "max_vibration", "max_tilt_angle")

# Write to gold layer
bridge_metrics.writeStream \
    .format("parquet") \
    .option("path", f"{gold_dir}/bridge_metrics") \
    .option("checkpointLocation", "checkpoints/gold_bridge_metrics") \
    .outputMode("append") \
    .start()

spark.streams.awaitAnyTermination()
