# from itertools import izip
import pandas as pd
import pdb


def table_ready_1loop(list_hex):
    '''create "background-color:#HEXCODE;" for each hex code'''
    col = ["'background-color:"+x+";'" for x in list_hex]
    return col


def table_ready_2loops(list_hex):
    '''create "background-color:#HEXCODE;" for each hex code'''
    col = ["'background-color:"+x+";'" for item in list_hex for x in item]
    return col


def html_ready(list_col1, name_col1, dtype_col1, list_col2, name_col2,
               dtype_col2):
    df = pd.DataFrame({name_col1: pd.Series(list_col1),
                      name_col2: pd.Series(list_col2)})
    df = df.astype(dtype={name_col1: "str", name_col2: "str"})
    return [dict(name_col1=u, name_col2=s) for u, s in zip(df[name_col1],
                                                           df[name_col2])]
