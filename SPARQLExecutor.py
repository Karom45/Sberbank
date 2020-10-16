#!/usr/bin/env python
# coding: utf-8

# In[1]:


from SPARQLWrapper import SPARQLWrapper, JSON
from fake_useragent import UserAgent

class SPARQLExecutor(object):
    def __init__(self, endpoint="https://query.wikidata.org/sparql", simplified: bool = True):
        self.sparql = SPARQLWrapper(endpoint , agent = UserAgent().random)
        self.sparql.setReturnFormat(JSON)
        self.simplified = simplified

    def execute(self, query, **params):
        if params:
            self.sparql.setQuery(query.format(**params))
        else:
            self.sparql.setQuery(query)
        results = self.sparql.query().convert()
        results = results['results']['bindings']
        if not self.simplified:
            return results
        else:
            return [{k: v['value'] for k, v in answer.items()} for answer in results]


# In[ ]:




