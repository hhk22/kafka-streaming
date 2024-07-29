# Spark Streaming

KaKao Api -> protobuf -> Spark streaming (consumer)

Naver Api -> protobuf -> Spark streaming (consumer)


# Installation

```
pip install -r requirements.txt

docker-compose up -d

# if topic doesn't exist
docker-compose exec kafka kafka-topics --create --topic book --bootstrap-server kafka:9092

# proto compile
protoc -I=./ --python_out=./ ./proto/book_data.proto

# proto buffer descriptor
protoc -o proto/book_data.desc proto/book_data.proto

python consumer/spark_streaming.py

```