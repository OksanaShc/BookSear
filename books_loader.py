import os
import sys
from elasticsearch import Elasticsearch
reload(sys)
sys.setdefaultencoding("utf-8")


def load_files():

    for book in os.listdir("./books/"):
        with open("./books/" + book) as new_file:
            data = new_file.read()
            es = Elasticsearch([{'port': 9123}])
            es.bulk(body=data.lower())

if __name__ == "__main__":
    load_files()