import colorsys
# from flask_table import Col
# from flask_table import create_table
# from flask_table import Table
import math
import pandas as pd
import pdb
# import webcolors


def table_ready_1loop(list_hex):
    '''create "background-color:#HEXCODE;" for each hex code'''
    col = ["background-color:"+x+";" for x in list_hex]
    return col


def table_ready_2loops(list_hex):
    '''create "background-color:#HEXCODE;" for each hex code'''
    col = ["background-color:"+x+";" for item in list_hex for x in item]
    return col


def step(r, g, b, reps=1):
    lum = math.sqrt(0.241 * r + .691 * g + .068 * b)
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    h2 = int(h * reps)
    lum2 = int(lum * reps)
    v2 = int(v * reps)
    if h2 % 2 == 1:
        v2 = reps - v2
        lum = reps - lum2
    return (h2, lum, v2)


def html_ready(list_col1, name_col1, dtype_col1, list_col2, name_col2,
               dtype_col2):
    df = pd.DataFrame({name_col1: pd.Series(list_col1),
                      name_col2: pd.Series(list_col2)})
    df = df.astype(dtype={name_col1: "str", name_col2: "str"})
    df['hex'] = df['codes'].replace(to_replace="[#]", value="",
                                    regex=True).astype(str)
    df['rgb'] = df['hex'].apply(lambda x: tuple(int(x[i:i+2], 16) for i in (0, 2, 4)))
    df['hsv'] = df['rgb'].apply(lambda rgb: step(rgb[0], rgb[1], rgb[2], 8))
    df.sort_values('hsv', inplace=True, ascending=True)
    df = df.drop(['hex', 'rgb', 'hsv'], axis=1)
    df = df.reset_index(drop=True)
    df['id'] = df.index
    df.set_index('id', inplace=True)
    old = [dict(name_col1=u, name_col2=s) for u, s in zip(df[name_col1],
                                                          df[name_col2])]
    df['id'] = df.index
    df = df.reset_index(drop=True)
    # pdb.set_trace()
    n2 = [dict(id=i, name_col1=u, name_col2=s) for i, u, s in zip(df['id'],
                                                                  df['colors'],
                                                                  df['codes'])]
    return old
