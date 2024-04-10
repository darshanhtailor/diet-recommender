import numpy as np
import re
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import NearestNeighbors
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer

def scaling(df):
    scaler=StandardScaler()
    prep_data=scaler.fit_transform(df.iloc[:,4:13].to_numpy())
    return prep_data,scaler

def nn_predictor(prep_data):
    neigh = NearestNeighbors(metric='cosine',algorithm='brute')
    neigh.fit(prep_data)
    return neigh

def build_pipeline(neigh,scaler,params):
    transformer = FunctionTransformer(neigh.kneighbors,kw_args=params)
    pipeline=Pipeline([('std_scaler',scaler),('NN',transformer)])
    return pipeline

def apply_pipeline(pipeline,_input,extracted_data):
    return extracted_data.iloc[pipeline.transform(_input)[0]]

def extract_data(df, max_list, ingredient_filter):
    extracted_data=df.copy()
    for column,maximum in zip(extracted_data.columns[4:13],max_list):
        extracted_data=extracted_data[extracted_data[column]<maximum]

    if ingredient_filter!=None:
        for ingredient in ingredient_filter:
            extracted_data=extracted_data[extracted_data['RecipeIngredientParts'].str.contains(ingredient,regex=False)] 
    return extracted_data


def recommend(df, max_list, _input=None, ingredient_filter=None, params={'n_neighbors':10, 'return_distance':False}):
    extracted_data = extract_data(df, max_list, ingredient_filter)

    if _input is None:
        return extracted_data

    prep_data,scaler=scaling(extracted_data)
    neigh=nn_predictor(prep_data)
    pipeline=build_pipeline(neigh,scaler,params)

    # _input = extracted_data.iloc[0:1,4:13].to_numpy()

    return apply_pipeline(pipeline,_input,extracted_data)
