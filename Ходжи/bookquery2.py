#!/usr/bin/env python
# coding: utf-8

# In[ ]:


answer_qualif = '''SELECT ?list ?listLabel ?item ?itemLabel
WHERE{{
     BIND(wd:{entity_id} as ?show)
     BIND(p:P360 as ?p)
     BIND(ps:P360 as ?ps)
     BIND(pq:P39 as ?pq)
     ?show ?p [?ps ?list;
               ?pq ?item].
     SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru, en". }}
}}'''

answer = '''SELECT ?item ?itemLabel ?show ?showLabel
WHERE{{
  BIND(wd:{entity_id} as ?show)
  BIND(p:{prop_id} as ?p)
  BIND(ps:{prop_id} as ?ps)
    ?show ?p [?ps ?item];
    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru, en". }}
}}'''

