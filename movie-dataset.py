#%% 
import pandas as pd
import seaborn as sns
from pathlib import Path

fp_db = Path(r'/home/sqrx/Documents/Data/the-movies-dataset')

# %%

data = {}

for file in fp_db.rglob(r'*.csv'):
    file_name = file.name.rstrip('.csv')
    try:
        data[file_name] = pd.read_csv(file, low_memory=False)
    except:
        print(file_name)

for k, v in data.items():
    print(k)
    print(v.head(2))

# %%

def convert_magicstr2col(x:pd.DataFrame)->pd.DataFrame:
    x_obj = x.select_dtypes('object')
    y = x.select_dtypes(exclude='object')
    str_type = x_obj.iloc[0,:].map(is_magicstr)
    # return str_type
    y_arraydict = convert_arraydict(x_obj.loc[:,str_type == 'arraydict'])
    y_dict = convert_dict(x_obj.loc[:,str_type == 'dict'])
    # y_array = convert_array(x_obj.loc[:,str_type == 'array'])

    return pd.concat([y,y_arraydict, y_dict])

def convert_dict(x):
    pass

def is_magicstr(x):
    if type(x) is str:
        dict_start = x.find('{', 0, 3) != -1
        dict_end = x.find('}', -3) != -1
        array_start = x.find('[', 0, 3) != -1
        array_end = x.find(']', -3) != -1

        if all([dict_start, dict_end, array_start, array_end]):
            return 'arraydict'
        elif dict_start & dict_end:
            return 'dict'
        # elif array_start & array_end:
        #     return 'array'
    return None

tt = [convert_magicstr2col(data[k].head()) for k in data.keys()]

print(tt)

# %%
