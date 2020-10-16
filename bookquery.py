#query.py

# Постараюсь описать пошагово: объясню КАЖДЫЙ аргумент:
# company - берем переменную и в нее запихиваем id книги(то есть для запроса надо подставить реальный Id)
# p - вернет характер отношений в виде p31(частный случай) или p18(картинка) , pLabel - ссылку на это
# statement - некая сущность , которая приводит нас всегда к текущей книге, хотя ссылки разные
# ps - продублирует p , но уже не относительно книги как объекта, а как ссылки , чтобы получить следующее значение
# ps_ - вернет саму сущность , если жанр - трагедия , если картинка - ссылка и тд
# wd - опять же возвращает , что и в p,но label вернет название этого отношения - жанр , изображение и тд
# то что в optional - вернет просто все qualifier для сущности(одно и тоже значение будет выводиться, пока не обрабоатет все qualifiers
query_from = """
    SELECT ?wd ?wdLabel ?ps_ ?ps_Label ?wd
    Label ?pq_Label ?direction {{
      VALUES (?company) {{(wd:{book_id})}}

      ?company ?p ?statement .
      ?statement ?ps ?ps_ .

      ?wd wikibase:claim ?p.
      ?wd wikibase:statementProperty ?ps.

      OPTIONAL {{
      ?statement ?pq ?pq_ .
      ?wdpq wikibase:qualifier ?pq .
      }}.
      BIND ("from" AS ?direction).
      SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru, en" }}
    }} ORDER BY ?wd ?statement ?ps_
    """
# Тут уже рассматриваем случае, когда объект упомнянается в других статья
# obj - где упомянается
# prop_id  - предикат (аналог p)
# book - сама книга
                                                             
query_to = '''
SELECT  ?obj ?objLabel ?wd ?prop_label ?bookLabel ?direction ?prop_id ?prop_idLabel
	WHERE {{
	  VALUES (?book) {{(wd:{book_id})}}.
	  ?obj ?prop_id ?book.
	  ?wd wikibase:directClaim ?prop_id.
	  ?wd rdfs:label ?prop_label.
	  FILTER((LANG(?prop_label)) = "ru").
    BIND ("to" AS ?direction).
	  SERVICE wikibase:label {{bd:serviceParam wikibase:language "ru, en" }} 
	}}
	ORDER BY ?obj
'''

entity_finding = '''
Select ?item ?itemLabel ?showLabel WHERE{{ BIND(wd:{entity_id} as ?show)
  ?item p:P31/ps:P31 ?show;
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru , en". }}
}}
limit 40000
'''

entity_finding_2 = '''
Select ?item ?itemLabel ?showLabel WHERE{{ BIND(wd:{entity_id} as ?show)
  ?item wdt:P31/wdt:P279* ?show;
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru , en". }}
}}
limit 40000
'''

subclass_entity_finding = '''
SELECT ?item ?itemLabel WHERE{{ BIND(wd:{entity_id} as ?show)
?item wdt:P279 ?show;
SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], en, ru". }}
}}
'''

counter_from = '''
SELECT (COUNT(?wd) AS ?countOut){{
		 	  VALUES (?company) {{(wd:{entity_id})}}

		      ?company ?p ?statement .
		      ?statement ?ps ?ps_ .

		      ?wd wikibase:claim ?p.
		      ?wd wikibase:statementProperty ?ps.
		    }} 
'''

counter_to = '''
SELECT  (COUNT(?obj) AS ?countIn) 
			WHERE {{
			  VALUES (?book) {{(wd:{entity_id})}} .
			  ?obj ?prop_id ?book.
			  ?wd wikibase:directClaim ?prop_id.
			  ?wd rdfs:label ?prop_label.
			  FILTER((LANG(?prop_label)) = "ru").
			}}
'''

finding_ID = '''
SELECT  ?propLabel{{
                VALUES (?prop_id) {{(wd:{entity_id})}}
			  ?prop wdt:P31/wdt:P279* ?prop_id.
               SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru,en". }}
			}}
'''

huge_entity_finding = '''
SELECT ?item WHERE{{ BIND(wd:{entity_id} as ?show)
    ?item wdt:P31 ?show;
}}
'''

all_predicates = '''SELECT ?property  ?propertyLabel ?propertyDescription ?propertyAltLabel WHERE {
  ?property wikibase:propertyType ?propertyType .
  SERVICE wikibase:label { bd:serviceParam wikibase:language "ru,en". }
}
ORDER BY ASC(xsd:integer(STRAFTER(STR(?property), 'P')))'''

rus_names = '''Select ?item ?itemLabel  WHERE{{ BIND(wd:{entity_id} as ?item)
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru,en". }}
}}
'''
subclass_of = '''SELECT ?show ?showLabel ?subclass ?subclassLabel
WHERE
{{ BIND(wd:{entity_id} as ?show).
?show wdt:P31 ?subclass
SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ru, en". }}
}}
'''

subclass_name = '''SELECT ?show ?showLabel
WHERE
{{ BIND(wd:{entity_id} as ?show).
SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE], ru, en". }}
}}
'''

qualifier_finder = '''
SELECT ?unit ?unitLabel 
WHERE
{{
  BIND(p:{property_id} as ?value)
  BIND(psv:{property_id} as ?value_s)
  BIND(wd:{entity_id} as ?item)
  
  ?item          ?value                     ?stmnode.   
  ?stmnode       ?value_s                   ?valuenode.
  ?valuenode     wikibase:quantityUnit       ?unit.
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru". }}
}} 
'''
subclass_of_3 = '''SELECT ?subclass ?subclassLabel ?show ?showLabel
WHERE
{{ BIND(wd:{entity_id} as ?show).
?show wdt:P279 ?subclass
SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru". }}
}}
'''

subclass_with_parents = '''SELECT ?parent ?parentLabel ?show ?showLabel
WHERE
{{ BIND(wd:{entity_id} as ?subclass).
?show wdt:P279* ?subclass.
?show wdt:P279 ?parent
SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru,en". }}
}}'''

subclass_entity_count = ''' SELECT (COUNT(?entity) AS ?entitycount)
WHERE {{ BIND(wd:{entity_id} as ?show).
?entity wdt:P31 ?show
}}
'''

predicat_reciver = '''SELECT ?item ?itemLabel ?an
{{BIND(wd:{entity_id} as ?item)
  BIND(wdt:{pred_id} as ?pred)
  ?item ?pred ?answer.
 SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru,en". }}
}}'''

leaders = '''SELECT  DISTINCT ?leader {{
        BIND (wd:{entity_id} as ?country)
		{{?country p:P35  [ps:P35 ?leader].}}
        UNION
        {{?country p:P6  [ps:P6 ?leader].}}
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru,en"}}
        }}'''

leaders_position = '''SELECT  DISTINCT ?person ?personLabel ?position ?positionLabel ?startTime ?startTimeNode ?endTime ?endTimeNode
        where{{
        BIND (wd:{entity_id}  as ?person)
        BIND (wd:{country_id}  as ?country)
		?person p:P39 ?pos.
        ?pos ps:P39 ?position.
        ?position wdt:P17 ?country.
        OPTIONAL{{?pos pq:P580 ?startTime;
                           pqv:P580 ?startTimeNode
                }}
        OPTIONAL{{?pos pq:P582 ?endTime;
                           pqv:P582 ?endTimeNode}}
        SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru,en"}}
        }}'''

labels = '''
SELECT ?qid ?qidLabel WHERE {{
  VALUES ?qid {{ {qid} }}.
  SERVICE wikibase:label {{ bd:serviceParam wikibase:language "ru,en". }}
}}'''