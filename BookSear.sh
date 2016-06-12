#!/bin/bash
bash  elasticsearch/bin/elasticsearch -d
echo 'elasticsearch running'
echo "WAIT PLEASE"
sleep 10
echo 'Loading books to elasticsearch'
python books_loader.py
sleep 5
python manage.py test -v 2 | tee "test_report.log"
python manage.py runserver



