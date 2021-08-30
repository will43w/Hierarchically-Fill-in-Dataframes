#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from fuzzywuzzy import process, fuzz
import re

df1 = pd.read_xyz("sample file1.xyz") # lowest priority dataframe
df2 = pd.read_xyz("sample file2.xyz") # middle ------------------
df3 = pd.read_xyz("sample file3.xyz") # highest ------------------

def is_match(name1, name2, tolerance = 75):
    if set(re.findall('\d+', name1)) == set(re.findall('\d+', name2)): # all numbers in string must be same
        if set([x.strip() for x in re.findall(r'(?i)\s[a-z]\s', name1 + ' ')]) == set([x.strip() for x in re.findall(r'(?i)\s[a-z]\s', name2 + ' ')]): # all isolated letters must be the same (vitamin d is too close to vitamin a otherwise)
            score = fuzz.token_sort_ratio(name1, name2)
            if score > tolerance:
                return True

for u_index, u_row in df2.iterrows(): # middle priority dataframe
    for l_index, l_row in df1.iterrows(): # lowest priority dataframe
        if is_match(u_row['Name'], l_row['Name']): # 'Name' column should be replaced to column along which the criterion for a match is contained ***
            for col_name, u_value in u_row.iteritems():
                if pd.isnull(u_value):
                    df2.loc[u_index][col_name] = l_row[col_name]
            df1.drop(l_index, inplace = True)
            break

for u_index, u_row in df3.iterrows(): # 2nd priority dataframe
    for l_index, l_row in df2.iterrows(): # lowest priority dataframe
        if is_match(u_row['Name'], l_row['Name']): # 'Name' column should be replaced to the column along which a fuzzy match is considered a (partially) redundant
            for col_name, u_value in u_row.iteritems():
                if pd.isnull(u_value):
                    df3.loc[u_index][col_name] = l_row[col_name]
            df2.drop(l_index, inplace = True)
            break
            
df_concat = pd.concat([df3, df2, df1]).reset_index(inplace = True)
df_concat.to_xyz("df_concat", index = False)

"""
*** e.g. for my case, it was multiple web-scrapes of a specific class of products, so if the products had the same name,
they were considered the same product, i.e. a match for the 'Name' column meant that these fields were for the same product,
but on two different websites i.e. why they're on different scrape results files
"""


