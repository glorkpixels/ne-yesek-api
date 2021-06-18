# import necessary libraries

# --------------------------- FLASK API IMPORTS START-------------------------------
from flask import Flask
from flask_restful import Resource, Api, reqparse
from flask import request
# --------------------------- FLASK API IMPORTS END-------------------------------


# --------------------------- FIREBASE LEARNING IMPORTS START-------------------------------
from firebase import firebase
from firebase.firebase import FirebaseApplication
from firebase.firebase import FirebaseAuthentication
firebase = firebase.FirebaseApplication('https://ne-yesek-ebf2f-default-rtdb.europe-west1.firebasedatabase.app/', None)
# --------------------------- FIREBASE IMPORTS END -------------------------------

# --------------------------- MACHINE LEARNING IMPORTS START-------------------------------
from pandas import DataFrame
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from ast import literal_eval
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn import metrics
import pandas as pd
import ast
import random
import numpy as np
import json

# --------------------------- MACHINE LEARNING IMPORTS END -------------------------------


app = Flask(__name__)
api = Api(app)

def get_user_cellar_from_firebase(UserKey):
    
    result = firebase.get('/UserCellarList/CnL9JzPEZLaDynXK1Qdbr3aiJEA3', None)
    


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
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(cuisine)
    tfidf_matrix.shape
    #feature_names = tfidf.get_feature_names()
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(foods.index, index=foods['Keys'])
    idx = indices[selectedrecipe]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores.sort(key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:5]
    ingredient_indices = [i[0] for i in sim_scores]
    result = foods['Keys'].iloc[ingredient_indices].to_json(orient="split")
    parsed = json.loads(result)
    #json.dumps(parsed, indent=4) 
    
    return parsed



def cuisine_based_recommendation(selectedcuisine):
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
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(cuisine)
    tfidf_matrix.shape
    #feature_names = tfidf.get_feature_names()
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(foods.index, index=foods['Keys'])
    idx = indices[selectedcuisine]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores.sort(key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:5]
    cuisine_indices = [i[0] for i in sim_scores]
    result = foods['Keys'].iloc[cuisine_indices].to_json(orient="split")
    parsed = json.loads(result)

    return parsed

def main_category_based_recommendation(selectedmaincategory):
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
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(cuisine)
    tfidf_matrix.shape
    #feature_names = tfidf.get_feature_names()
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(foods.index, index=foods['Keys'])
    idx = indices[selectedmaincategory]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores.sort(key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:5]
    main_category_indices = [i[0] for i in sim_scores]
    result = foods['Keys'].iloc[main_category_indices].to_json(orient="split")
    parsed = json.loads(result)
    
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
    

class RecommendationLive(Resource):
    # Write method to fetch data from the CSV file
    def get(self):
        userKey = request.args.get("UserKey")
        userPreferences= request.args.get("UserPref")
        
        mealDay = request.args.get("MealDay")       
        
        mealList= [] 
        breakfastBool = request.args.get("Breakfast")
        lunchBool = request.args.get("Lunch")
        dinnerBool = request.args.get("Dinner")
        
        homeIngres = request.args.get("HomeIngredients")
        
        
        if mealDay == 1:
            if breakfastBool == 1 and lunchBool ==1 and dinnerBool ==1:
                if homeIngres ==1:
                    print("Home")
                    if userPreferences ==1:
                        pass
                else:
                    if userPreferences ==1:
                        pass
                    
            elif breakfastBool == 1 and lunchBool ==1 and dinnerBool ==0:
                if homeIngres ==1:
                    print("Home")
                    if userPreferences ==1:
                        pass
                else:
                    if userPreferences ==1:
                        pass
                    
            elif breakfastBool == 1 and lunchBool ==0 and dinnerBool ==1:
                if homeIngres ==1:
                    print("Home")
                    if userPreferences ==1:
                        pass
                else:
                    if userPreferences ==1:
                        pass
            
            elif breakfastBool == 0 and lunchBool ==1 and dinnerBool ==1:
                if homeIngres ==1:
                    print("Home")
                    if userPreferences ==1:
                        pass
                else:
                    if userPreferences ==1:
                        pass
                    
        if mealDay == 2:
            pass
        if mealDay == 3:
            pass

        
        return "fuck"

    def post(self):
    # Write method to write data to the CSV file
        return "this is a recommendation post req"
    

class RecommendationOneMeal(Resource):
    # Write method to fetch data from the CSV file
    def get(self):
        userKey = request.args.get("UserKey")
        userPreferences= request.args.get("UserPref")
        homeIngres = request.args.get("HomeIngredients")
        mealSelection = request.args.get("MealSelect")
        
        
        var = '{ "One Meal": "' + userKey + userPreferences + homeIngres + mealSelection +'"}'

        y = json.loads(var)
        
        
        return y

    def post(self):
    # Write method to write data to the CSV file
        return "this is a recommendation post req"    


api.add_resource(Hello, '/hello')
api.add_resource(Recommendation, '/recommendation')
api.add_resource(RecommendationLive, '/recommendalive')
api.add_resource(RecommendationOneMeal, '/recommendonemeal')


if __name__ == '__main__':
    app.run()  # run our Flask app
    
    