# %%
from SPARQLExecutor import SPARQLExecutor
import bookquery
import pandas as pd
from pathlib import Path
from tqdm import tqdm

data_dir = Path.cwd() / 'csv' 
executor = SPARQLExecutor()

def create_chunks(list_name, n):
    for i in range(0, len(list_name), n):
        yield list_name[i:i + n]

# %%
qids = list(pd.read_excel(data_dir/ 'auto_countries.xlsx')['QID исторической страны'])
# %%
# print(create_chunks(qids , 100))
# %%
main_lst = []
for chunk in tqdm(create_chunks(qids, 50)):
    # print(chunk)
    instanceOf = executor.execute(bookquery.instance_of , qid=' '.join(f'wd:{qid}' for qid in chunk))
    main_lst.extend(instanceOf)
instanceOf_lst = pd.DataFrame(main_lst)
instanceOf_lst.drop_duplicates(inplace = True)
instanceOf_lst.to_excel(data_dir / 'instances_of_countries_list.xlsx' ,encoding='utf-8-sig' , index = False)
# %%
main_lst = []
for chunk in tqdm(create_chunks(qids, 50)):
    # print(chunk)
    subclassOf = executor.execute(bookquery.subclass_of , qid=' '.join(f'wd:{qid}' for qid in chunk))
    main_lst.extend(subclassOf)
subclassOf_lst = pd.DataFrame(main_lst)
subclassOf_lst.drop_duplicates(inplace = True)
subclassOf_lst.to_excel(data_dir / 'subclass_of_countries_list.xlsx' ,encoding='utf-8-sig' , index = False)
# %%
main_lst = []
for chunk in tqdm(create_chunks(qids, 50)):
    # print(chunk)
    subclassOf_with_entites = executor.execute(bookquery.subclass_of_with_entities , qid=' '.join(f'wd:{qid}' for qid in chunk))
    main_lst.extend(subclassOf_with_entites)
subclassOf_with_entites_lst = pd.DataFrame(main_lst)
subclassOf_with_entites_lst.drop_duplicates(inplace = True)
subclassOf_with_entites_lst.to_excel(data_dir / 'subclass_of_countries_with_entites_list.xlsx' ,encoding='utf-8-sig' , index = False)
# %%
main_lst = []
for chunk in tqdm(create_chunks(qids, 50)):
    # print(chunk)
    instanceOf_with_entities = executor.execute(bookquery.instance_of_with_entities , qid=' '.join(f'wd:{qid}' for qid in chunk))
    main_lst.extend(instanceOf_with_entities)
instanceOf_with_entities_lst = pd.DataFrame(main_lst)
instanceOf_with_entities_lst.drop_duplicates(inplace = True)
instanceOf_with_entities_lst.to_excel(data_dir / 'instance_of_countries_with_entites_list.xlsx' ,encoding='utf-8-sig' , index = False)
# %%
