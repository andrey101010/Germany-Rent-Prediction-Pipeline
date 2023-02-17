# %%
import pandas as pd
import numpy as np

# %%
# read the housing data file
housing_orig_df = pd.read_csv(r'../data/housing_data_hamburg.txt', sep = '\t')
#housing_orig_df.head()
# %%
def get_unique_details(details_column):
    """
    produce a set of unique word used to describe a property ad
    Input: pandas data base column with details
    Output: set with unique descriptions

    """
    unique_details = set() 
    for details in details_column:
        list_details = details.split(', ')
        for ld in list_details:
            unique_details.add(ld)
    remove_words = {'...', 'No extra details'}
    unique_details = unique_details.difference(remove_words) # remove unwanted words
    return unique_details

unique_details_new = get_unique_details(housing_orig_df['Extra details']) 
print(unique_details_new) # print the features
# %%
def detail_dataframe_creator(original_df, unique_details_set):
    """
    create a new dataframe with the unique details as columns
    """
    df = pd.DataFrame(columns=unique_details_set)
    output_df = pd.concat([original_df, df])
    return output_df

new_df = detail_dataframe_creator(housing_orig_df, unique_details_new)
#new_df.head()
# %%
def create_final_df(input_df, unique_set):
    """
    Check if the description of each apartment with the list and if the 
    descrition exist adds 1 to the corresponding column
    Input: Updated dataframe, feature set
    Output: Dataframe with one hot encoding

    """
    for i in range(len(input_df['Extra details'])):
        for element in set(unique_set).intersection(input_df['Extra details'][i].split(', ')):
            input_df[element][i] = 1
    input_df.replace(np.nan, 0, inplace=True)
    return input_df.drop(columns=['Extra details'], inplace=True)
    
final_df = create_final_df(new_df, unique_details_new)
# new_df.head()
new_df.to_csv(r'../data/housing_data_hamburg_df.csv')
# new_df['Balkon'].value_counts()
# %%
