import os
import sys
import requests
import json
import time
from dotenv import load_dotenv

package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

from confluent_kafka import Producer
import proto.book_data_pb2 as pb2
from keywords import book_keywords

load_dotenv()

def get_original_data(query: str) -> dict:
    api_key = os.environ.get("KAKAO_APi_KEY")
    url = "https://dapi.kakao.com/v3/search/book"

    res = requests.get(
        url=url,
        headers={
            "Authorization": f"KakaoAK {api_key}"
        },
        params={
            "query": query,
            "size": 50,
            "page": 1
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
        for item in original_data['documents']:
            book = pb2.Book()
            book.title = item['title']
            book.author = ','.join(item['authors'])
            book.publisher = item['publisher']
            book.isbn = item['isbn']
            book.price = int(item['price'])
            book.publication_date = item['datetime']
            book.source = "kakao"
            # print("=====")
            # print(book)
            # print("=====")
            producer.produce(topic="book", value=book.SerializeToString())
            producer.flush()

        print(f"keyword({keyword}) 전송 완료!")
        time.sleep(3)