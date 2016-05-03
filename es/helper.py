import logging
import sys
from elasticsearch import Elasticsearch
reload(sys)
sys.setdefaultencoding("utf-8")

logging.basicConfig(format=u'%(levelname)-8s [%(asctime)s] %(message)s', level=logging.INFO,
                    filename=u'search_result.log')
logger = logging.getLogger('elasticsearch.trace')
logger.addHandler(logging.NullHandler())
logger.setLevel(logging.INFO)


class ElasticHelper(object):
    @staticmethod
    def _send_es_request(text):
        es = Elasticsearch([{'port': 9123}])
        results = es.search(body={"query": {"match_phrase_prefix": {"text": text.lower()}}})
        logging.info("Search text: '%s'.Search took: %s ms" % (text, results['took']))
        return results

    @staticmethod
    def _create_message(results, text):
        if results[u'hits'][u'total'] > 0:
            message = 'Text "%s" was found in:\n' % text
            for result in sorted(results[u'hits'][u'hits']):
                message += 'book %s %s page %s\n' % (result[u'_index'], result['_type'], result['_id'])
        else:
            message = 'Text "%s" not found' % text
        return message

    def make_search(self, text):
        results = self._send_es_request(text)
        message = self._create_message(results, text)
        return message

