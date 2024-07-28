import os
import sys
import requests
import json
import time
from dotenv import load_dotenv

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(package_path)

from confluent_kafka import Producer
import proto.book_data_pb2 as pb2
from keywords import book_keywords

load_dotenv()

def get_original_data(query: str) -> dict:
    client_id = os.environ.get("NAVER_CLIENT_ID")
    client_secret = os.environ.get("NAVER_CLIENT_SECRET")
    url = "https://openapi.naver.com/v1/search/book.json"

    res = requests.get(
        url=url,
        headers={
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret,
        },
        params={
            "query": query,
            "display": 100,
            "start": 1
        }
    )

    if res.status_code >= 400:
        raise Exception(res.content)

    return json.loads(res.text)


if __name__ == '__main__':
    conf = {
        'bootstrap.servers': 'localhost:29092',
    }

    producer = Producer(conf)
    topic = "book"

    for keyword in book_keywords:
        original_data = get_original_data(keyword)
        print(original_data.keys())
        for item in original_data['items']:
            book = pb2.Book()
            book.title = item['title']
            book.author = ','.join(item['author'])
            book.publisher = item['publisher']
            book.isbn = item['isbn']
            book.price = int(item['discount'])
            book.publication_date = item['pubdate']
            book.source = "naver"
            # print("=====")
            # print(book)
            # print("=====")
            producer.produce(topic="book", value=book.SerializeToString())
            producer.flush()

        print(f"keyword({keyword}) 전송 완료!")
        time.sleep(3)