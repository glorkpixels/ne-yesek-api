from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import request
import pandas as pd
import ast
import pandas as pd
# import necessary libraries
import random
import numpy as np

import json
# Models
from pandas import DataFrame
# Content-Based Recommendation (Description Only) Term Frequency-Inverse Document Frequency Vectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
# Content-Based Recommendation Linear Kernel for Cosine Similarity
from sklearn.metrics.pairwise import linear_kernel
# Content-Based Recommendation Parsing the stringified features into their corresponding python objects
from ast import literal_eval
# Content-Based Recommendation CountVectorizer  for Creation of the Count Matrix
from sklearn.feature_extraction.text import CountVectorizer
# Content-Based Recommendation Computation of the Cosine Similarity Matrix Based
from sklearn.metrics.pairwise import cosine_similarity

from sklearn.model_selection import train_test_split
from sklearn import metrics



app = Flask(__name__)
api = Api(app)




def ingredient_based_recommendation(selectedrecipe):
    foodsx = pd.read_json (r'ultimate_food.json')
    foods = foodsx.T
    leng =len(foods.index)
    indexes = []
    p = foods.index.values
    foods.insert( 0, column="Keys",value = p)
    for i in range(0,leng):
        indexes.append(i)
    
    foods["Index"] = indexes
    foods = foods.set_index("Index")   
    cuisine = foods["IngridientNames"]

    # Define a TF-IDF Vectorizer Object. Remove all english stop words such as 'the', 'a'
    tfidf = TfidfVectorizer(stop_words='english')  # This was used first which is correct.
    # tfidf = TfidfVectorizer(analyzer='word',ngram_range=(1, 2),min_df=0,stop_words='english') #This is an alternative of the above.

    # Replace NaN with an empty string
    # descriptions = descriptions.fillna('')

    # Construct the required TF-IDF matrix by fitting and transforming the data
    tfidf_matrix = tfidf.fit_transform(cuisine)
    # print(tfidf_matrix)

    # Output the shape of tfidf_matrix
    tfidf_matrix.shape
    # print(tfidf_matrix.shape)

    # all the words in descriptions
    feature_names = tfidf.get_feature_names()
    # print(feature_names)

    # Compute the cosine similarity matrix
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    #print(cosine_sim)
    """print(cosine_sim.shape)
    print(cosine_sim[2])"""

    # Construct a reverse map of indices and movie titles
    indices = pd.Series(foods.index, index=foods['Keys'])
    #print(indices)  # indices can be incremented 1

    # Get the index of the movie that matches the title
    idx = indices[selectedrecipe]
    # Get the pairwsie similarity scores of all movies with that movie
    sim_scores = list(enumerate(cosine_sim[idx]))
    # Sort the movies based on the similarity scores
    sim_scores.sort(key=lambda x: x[1], reverse=True)

    # Get the scores of the 10 most similar movies
    sim_scores = sim_scores[1:5]

    # Get the movie indices
    cuisine_indices = [i[0] for i in sim_scores]
    
    result = foods['Keys'].iloc[cuisine_indices].to_json(orient="split")
    parsed = json.loads(result)
    #json.dumps(parsed, indent=4) 
    
    # Return the top 10 most similar movies
    
    return parsed


class Hello(Resource):
    # Write method to fetch data from the CSV file
    def get(self):
        return "this is a get req"

    def post(self):
    # Write method to write data to the CSV file
        return "this is a post req"
    
class Recommendation(Resource):
    # Write method to fetch data from the CSV file
    def get(self):
        reckey = request.args.get("RecipeKey")
        recomm = ingredient_based_recommendation(reckey)
        return recomm

    def post(self):
    # Write method to write data to the CSV file
        return "this is a recommendation post req"
    
    
    


api.add_resource(Hello, '/hello')
api.add_resource(Recommendation, '/recommendation')

if __name__ == '__main__':
    app.run()  # run our Flask app
    
    