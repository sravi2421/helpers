import pandas as pd
import numpy as np


def top_categoricals(df, categ_cols):
    '''
    takes a df and a list of categorical columns, returns a data frame which contains value counts
    for each categorical column
    
    Args:
        df (pandas dataframe):   dataframe of interest
        categ_cols (list):       list of categorical columns to contain in summary

    Returns:
        summary_table (pandas df):  dataframe containing values and counts
    '''
    if len(set(categ_cols))!=len(categ_cols):
            assert False, 'Ensure no column is repeated'
    total_obs = df.shape[0]
    categ_counts = {col: (list(df[col].value_counts().index[:5]), list(df[col].value_counts()[:5])) for col in categ_cols}
    pd_categ_vals = {categ+'_val':categ_counts[categ][0] for categ in categ_counts}
    pd_categ_counts = {categ+'_count':categ_counts[categ][1] for categ in categ_counts}
    pd_categ_vals = fill_dict_lists(pd_categ_vals)
    pd_categ_counts = fill_dict_lists(pd_categ_counts)

    col_order = []
    for col in categ_cols:
        ##Fill null count
        pd_categ_vals[col+'_val'].append('Null')
        pd_categ_counts[col+'_count'].append(df[col].isnull().sum())
        ##order the columns correctly
        col_order.append(col+'_val')
        col_order.append(col+'_count')
        col_order.append(col+'_prop')
    summary_table = pd.DataFrame(data = {**pd_categ_counts, **pd_categ_vals})
    
    prop_cols = (
        (summary_table[pd_categ_counts.keys()]/total_obs)
        .rename(columns = {'{}_count'.format(col):'{}_prop'.format(col) for col in categ_cols}))
    return summary_table.join(prop_cols)[col_order]

def fill_dict_lists(dict_):
    '''
    cycle through keys in dictionary to ensure all lists are of the same length
    will fill any 'missing' entries with a null value
    args:
        dict_(dict): dict of the form {'key1':[er]}
    returns:
        dict_(dict): modified dictionary with lists of equal length
    '''
    max_l = max([len(dict_[key]) for key in dict_])
    for key in dict_:
        l = len(dict_[key])
        for _ in range(l, max_l):
            dict_[key].append(np.nan)
    return dict_