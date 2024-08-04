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

# Trouble Shooting

- Environment
    - Windows 11
    - Pyspark 3.4.1

- sys_path 에 등록되어있는 Hadoop path에 두개의 파일이 필요함. 
    - hadoop.dll
    - wintuils.exe

- pyspark를 깔더라도 필요한 jar파일들이 있음. 해당 파일들을 추가. 

    ```
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

    # 위의 방식대로 하거나, spark-submit에 args로 넣어주거나..
    # 아니면 site-packages/pyspark/jars 직접 받아서 추가해주거나..
    # --> https://mvnrepository.com/
    ```


