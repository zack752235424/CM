from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch()

doc = {
    'author': '赵二飞',
    'text': '准备回了',
    'timestamp': datetime.now(),
}
# res = es.index(index="test-index", doc_type='tweet', body=doc)
# print(res)


res1 = es.search(index='test-index', doc_type='tweet')
print(res1)

# res = es.get(index="test-index", doc_type='tweet', id=1)
# print(res['_source'])

# es.indices.refresh(index="test-index")

# res = es.search(index="test-index", body={"query": {"match_all": {}}})
# print("Got %d Hits:" % res['hits']['total']['value'])
# for hit in res['hits']['hits']:
#     print("%(timestamp)s %(author)s: %(text)s" % hit["_source"])

# result = es.indices.create(index='test')
# print(result)

# result = es.search(index='test', doc_type='politics')