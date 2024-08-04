from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.protobuf.functions import from_protobuf
import os

os.environ['PYSPARK_SUBMIT_ARGS'] = (
    '--packages '
    'org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.1,'
    'org.apache.kafka:kafka-clients:3.4.0,'
    'org.apache.spark:spark-streaming_2.12:3.4.1,'
    'org.apache.spark:spark-token-provider-kafka-0-10_2.12:3.4.1,'
    'org.apache.commons:commons-pool2:2.11.1,'
    'org.apache.spark:spark-protobuf_2.12:3.4.1 '
    'pyspark-shell'
)


if __name__ == '__main__':
    ss: SparkSession = SparkSession.builder \
        .master("local") \
        .appName("spark_kafka_ex") \
        .getOrCreate()

    proto_desc_path = "C:\\Users\\khhh9\\OneDrive\\Desktop\\kafka-streaming\\proto\\book_data.desc"

    df = ss \
        .readStream \
        .format("kafka") \
        .option("startingOffsets", "earliest") \
        .option("subscribe", "book") \
        .option("kafka.bootstrap.servers", "localhost:29092") \
        .load() \
        .select(from_protobuf("value", "Book", proto_desc_path).alias("book")) \
        .withColumn("title", F.col("book.title")) \
        .withColumn("author", F.col("book.author")) \
        .withColumn("publisher", F.col("book.publisher")) \
        .withColumn("price", F.col("book.price")) \
        .withColumn("publication_date", F.col("book.publication_date")) \
        .withColumn("source", F.col("book.source")) \
        .withColumn("processing_time", F.current_timestamp()) \
        .select("title", "author", "publisher", "price", "publication_date", "source",
                "processing_time")

    price_stat_df = \
        df.groupby(
            F.window(F.col("processing_time"), "1 minute"), "source").agg(
            F.max("price").alias("max_price"),
            F.min("price").alias("min_price"),
            F.mean("price").alias("mean_price")
        )

    price_stat_df.writeStream \
        .format("console") \
        .outputMode("complete") \
        .option("truncate", "false") \
        .start() \
        .awaitTermination()