*****************************************************
* ATTENTION: requires installed Java 8 with         *
* correct settings of system variables, Python 2.7, *
* Django1.9.5, elasticsearch-py 2.3.0               *
* The project was tested on Ubuntu and Mac Os       *
*****************************************************

Here is BookSear, my test work.

Requirements:
*Python 2.7
*Java 1.8 (necessary for ElasticSearch)
*framework   Django 1.9.5
    pip install Django==1.9.5
search engine: Elasticsearch 2.3.2 (there is at the project directory)
python client for Elasticsearch 2.3.0
    pip install elasticsearch

*****************************************************
* ATTENTION: Elasticsearch is run on 9123 port      *
* endpoint is http:\\localhost:9123                 *
*****************************************************

--------------- Run ---------------------------------- -------------------------------------
For installing the all components of project and tests you need install all clone the project from Github enter to the project and run bashscript BookSear.sh in the project folder.

1. git clone https://github.com/OksanaShc/BookSear.git
2. Go to the project's directory
3. Run the command at the commands line:

		./BookSear.sh

1. bash  elasticsearch/bin/elasticsearch -d
2.python books_loader.py
3. python manage.py test -v 2 | tee -a "test_report.log"
4. python manage.py runserver

Do not close terminal until you finished your work with app
----------------------------------- -------------- Reports -------------------------------------
Reporting are implemented via unittest framework
look test_report.log at project directory