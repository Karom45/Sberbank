# %%
from SPARQLExecutor import SPARQLExecutor
import bookquery
from pathlib import Path
from os.path import join,isfile
from os import listdir
import pandas as pd

def counter_for_files(path):
    
    """Подсчет файлов в директории"""
        
    onlyfiles = [join(path, f) for f in listdir(path) if isfile(join(path, f))]
    return onlyfiles

data_dir = Path.cwd() / 'wikipedia_countries' / 'excel'
# %%
executor = SPARQLExecutor()
for file in counter_for_files(data_dir)[5:6]:
    qids = set(pd.read_excel(file)['qid исторического государстава'])
    print(qids)
    labels = executor.execute(bookquery.labels , qid=' '.join(f'wd:{qid}' for qid in qids))
    labels = [item['qidLabel'] for item in labels]
    print(labels)
# %%
file  = Path.cwd() / 'csv' / 'auto_countries.xlsx'
df = pd.read_excel(file)
qids = df['QID метастраны'].dropna()
qids
executor = SPARQLExecutor()
labels = executor.execute(bookquery.labels , qid=' '.join(f'wd:{qid}' for qid in qids))
labels = {item['qid'].split('/')[-1] : item['qidLabel'] for item in labels}
# print(labels)
df['Метастрана rus'] = None
for k,v in df.iterrows():
    for key , value in labels.items():
        if v['QID метастраны'] == key:
            ind = list(df[df['QID метастраны'] == key].index)[0]
            df.loc[ind , 'Метастрана rus'] = value
df
df.insert(2, 'Метастрана_rus', df['Метастрана rus'])
# %%
df = df.drop(['Метастрана rus'] , axis = 1)
df.to_excel(file ,encoding='utf-8-sig' , index = False)
# %%

# %%
