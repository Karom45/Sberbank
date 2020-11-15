# %%
import pandas as pd
from pathlib import Path
from SPARQLExecutor import SPARQLExecutor
import bookquery
from tqdm import tqdm
executor = SPARQLExecutor()

def create_chunks(list_name, n):
    for i in range(0, len(list_name), n):
        yield list_name[i:i + n]

dir_with_graph =  Path.cwd() / 'csv' 
dir_with_dependencies =  Path.cwd() / 'graph' 
# %%
countries_df = pd.read_csv(dir_with_graph / 'countries.csv' , sep = ';')
countries_df = countries_df[~countries_df['country'].str.contains(r'_')]
# %%
qids = df[~df['country'].str.contains(r'_')]['country']
# %%
main_lst = []
for chunk in tqdm(create_chunks(qids, 50)):
    # print(chunk)
    instanceOf = executor.execute(bookquery.instance_of_with_entities , qid=' '.join(f'wd:{qid}' for qid in chunk))
    main_lst.extend(instanceOf)
instanceOf_lst = pd.DataFrame(main_lst)
instanceOf_lst.drop_duplicates(inplace = True)
# %%
instanceOf_lst
# %%
dependencies_qids = pd.read_excel(dir_with_dependencies / 'depended_countries_instance.xlsx')['subclass']
# %%
colonial_countries = instanceOf_lst[instanceOf_lst['instanceOf'].isin(dependencies_qids)]
# %%
colonial_countries.to_excel(dir_with_graph / 'colonies_with_instances.xlsx' , index = False)
# %%
colonies_df = pd.read_excel(dir_with_graph / 'colonies_with_instances.xlsx')
set(colonies_df['instanceOf'])
# %%
new_countries_df = countries_df.iloc[:,2:7]
# %%
new_colonies_df = colonies_df[['qid', 'ColonyOf']]
new_colonies_df.columns = ['country' , 'owner']
new_colonies_df
# %%
merged_df = pd.merge(new_colonies_df,new_countries_df).drop_duplicates()
merged_df
# %%
merged_df.to_excel(dir_with_graph / 'colonies_with_instances_merged.xlsx' , index = False)
# %%
