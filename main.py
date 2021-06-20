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
    
    result = firebase.get('/UserCellarList/'+UserKey, None)
    list_of_dict_values = list(result.values())

    FavIngres = []
    for i in list_of_dict_values:
        if i["name"] not in FavIngres:
            FavIngres.append(i["name"])
            
    ingridientList = list(dict.fromkeys(FavIngres))
    joined_string = ", ".join(ingridientList)   
    print(joined_string)
    return joined_string
    
    
def get_user_fav_recipes_from_firebase(UserKey):
    
    result = firebase.get('/UserFavorites/'+UserKey+'/Meals', None)
    #print(type(result))

    list_of_dict_values = list(result.values())
    #print(type(list_of_dict_values))
    
    FavIngres = []
    for i in list_of_dict_values:
        if i["mKey"] not in FavIngres:
            FavIngres.append(i["mKey"])
            
    ingridientList = list(dict.fromkeys(FavIngres))
    #print(ingridientList)
    return ingridientList

    
def get_user_fav_ingres_from_firebase(UserKey):
    result = firebase.get('/UserFavorites/'+UserKey+'/Ingredient', None)
    list_of_dict_values = list(result.values())
    FavIngres = []
    for i in list_of_dict_values:
        if i["mKey"] not in FavIngres:
            FavIngres.append(i["mKey"])
            
    ingridientList = list(dict.fromkeys(FavIngres))
    joined_string = ", ".join(ingridientList)   
    return joined_string


def ingredient_based_recommendation_recipe(selectedrecipe):
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
    
    return foods['Keys'].iloc[ingredient_indices]


def ingredient_based_recommendation(selectedcuisine):
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
    foods.loc[len(foods.index)] = ['Any','Any','Any','Any',selectedcuisine,'Any','Any','Any','Any','Any','Any','Any'] 
    cuisine = foods["IngridientNames"]
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(cuisine)
    tfidf_matrix.shape
    #feature_names = tfidf.get_feature_names()
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    indices = pd.Series(foods.index, index=foods['IngridientNames'])
    idx = indices[selectedcuisine]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores.sort(key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    cuisine_indices = [i[0] for i in sim_scores]
    result = foods['Name'].iloc[cuisine_indices].to_json(orient="split")
    parsed = json.loads(result)

    return foods['Keys'].iloc[cuisine_indices]

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

def breakfast_recommendation(title):
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

    features = ['CategoryBread']
    foods['soup'] = ''
    for feature in features:
        foods['soup'] += foods[feature]

    count = CountVectorizer(stop_words='english')  

    count_matrix = count.fit_transform(foods['soup'])
    print(count_matrix.shape)

    foods.reset_index()
    indices = pd.Series(foods.index, index=foods['CategoryBread'])
    idx = indices[title]
    print(i)
    randomch = random.choice(idx)
    result = foods.iloc[randomch][['Keys']].to_json(orient="split")
    parsed = json.loads(result)
 
    return foods.iloc[randomch][['Keys']]


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
        firebase.delete('/UserMenus/', userKey)  
        userPreferences= int(request.args.get("UserPref"))
        mealDay = int(request.args.get("MealDay"))   
    
        mealList= [] 
        breakfastBool = int(request.args.get("Breakfast"))
        lunchBool = int(request.args.get("Lunch"))
        dinnerBool = int(request.args.get("Dinner"))
        
        homeIngres = int(request.args.get("HomeIngredients"))
        ingredientsHome = get_user_cellar_from_firebase(userKey)
        ingredientsHome += ", " + get_user_fav_ingres_from_firebase(userKey)
        recipesliked = get_user_fav_recipes_from_firebase(userKey)
        choice = random.choices(recipesliked)

        if breakfastBool == 1 and lunchBool ==1 and dinnerBool ==1:
            if homeIngres ==1:
                ret = ingredient_based_recommendation(ingredientsHome)
                var = breakfast_recommendation('KAHVALTILIK TARİFLERİ')
                result = ret.to_json(orient="split")
                parsed = json.loads(result)
                print(ret.tolist())
                retlist = ret.tolist()
                breakfs = var.tolist()
                pop1 = retlist.pop(0)
                pop2 = retlist.pop(0)
                
                data =  { 
                        'Day' : 1,
                        'Breakfast' : breakfs[0],
                        'Lunch': pop1,
                        'Dinner': pop2
                        }
                result = firebase.post('/UserMenus/'+userKey+'/',data)
                daycount = 2
                if(mealDay >2):
                     for i in range(mealDay-1):
                        var = breakfast_recommendation('KAHVALTILIK TARİFLERİ')
                        breakfs = var.tolist()
                        
                        popped =retlist.pop(0)
                        list4=ingredient_based_recommendation_recipe(popped)
                        list4 = list4.tolist()
                        list4.pop(0)
                        list4.pop(0)
                        pop1 = list4.pop(0)
                        pop2 = list4.pop(0)
                        
                        data =  { 
                        'Day' : daycount,
                        'Breakfast' : breakfs[0],
                        'Lunch': pop1,
                        'Dinner': pop2
                        }
                        result = firebase.post('/UserMenus/'+userKey+'/',data)
                        daycount +=1
                
                print(pop1 + " xd" + pop2)
               
            else:

                print("lol")
                
        elif breakfastBool == 1 and lunchBool ==1 and dinnerBool ==0:
            if homeIngres ==1:
                ret = ingredient_based_recommendation(ingredientsHome)
                var = breakfast_recommendation('KAHVALTILIK TARİFLERİ')
                result = ret.to_json(orient="split")
                parsed = json.loads(result)
                print(ret.tolist())
                retlist = ret.tolist()
                breakfs = var.tolist()
                pop1 = retlist.pop(0)
                pop2 = retlist.pop(0)
                
                data =  { 
                         'Day' : 1,
                        'Breakfast' : breakfs[0],
                        'Lunch': pop1
                        }
                result = firebase.post('/UserMenus/'+userKey+'/',data)
                daycount = 2
                if(mealDay >2):
                     for i in range(mealDay-1):
                        var = breakfast_recommendation('KAHVALTILIK TARİFLERİ')
                        breakfs = var.tolist()
                        
                        popped =retlist.pop(0)
                        list4=ingredient_based_recommendation_recipe(popped)
                        list4 = list4.tolist()
                        list4.pop(0)
                        list4.pop(0)
                        pop1 = list4.pop(0)
                        pop2 = list4.pop(0)
                        
                        data =  { 
                                 'Day' : daycount,
                        'Breakfast' : breakfs[0],
                        'Lunch': pop1
                        }
                        
                        result = firebase.post('/UserMenus/'+userKey+'/',data)
                        daycount +=1
                
                print(pop1 + " xd" + pop2)
                
            else:
                #return(ingredient_based_recommendation_recipe(choice[0]))
                pass
        elif breakfastBool == 1 and lunchBool ==0 and dinnerBool ==1:
            if homeIngres ==1:
                ret = ingredient_based_recommendation(ingredientsHome)
                var = breakfast_recommendation('KAHVALTILIK TARİFLERİ')
                result = ret.to_json(orient="split")
                parsed = json.loads(result)
                print(ret.tolist())
                retlist = ret.tolist()
                breakfs = var.tolist()
                pop1 = retlist.pop(0)
                pop2 = retlist.pop(0)
                
                data =  { 
                         'Day' : 1,
                        'Breakfast' : breakfs[0],
                        'Dinner': pop2
                        }
                result = firebase.post('/UserMenus/'+userKey+'/',data)
                daycount = 2
                if(mealDay >2):
                     for i in range(mealDay-1):
                        var = breakfast_recommendation('KAHVALTILIK TARİFLERİ')
                        breakfs = var.tolist()
                        
                        popped =retlist.pop(0)
                        list4=ingredient_based_recommendation_recipe(popped)
                        list4 = list4.tolist()
                        list4.pop(0)
                        list4.pop(0)
                        pop1 = list4.pop(0)
                        pop2 = list4.pop(0)
                        
                        data =  { 
                                 'Day' : daycount,
                        'Breakfast' : breakfs[0],
                        'Dinner': pop2
                        }
                        
                        result = firebase.post('/UserMenus/'+userKey+'/',data)
                        daycount +=1
                
                print(pop1 + " xd" + pop2)
                
            else:
                return(ingredient_based_recommendation_recipe(choice[0]))
        
        elif breakfastBool == 0 and lunchBool ==1 and dinnerBool ==1:
            if homeIngres ==1:
                ret = ingredient_based_recommendation(ingredientsHome)
                result = ret.to_json(orient="split")
                parsed = json.loads(result)
                print(ret.tolist())
                retlist = ret.tolist()
                pop1 = retlist.pop(0)
                pop2 = retlist.pop(0)
                
                data =  { 
                         'Day' : 1,
                        'Lunch': pop1,
                        'Dinner': pop2
                        }
                result = firebase.post('/UserMenus/'+userKey+'/',data)
                daycount = 2
                if(mealDay >2):
                     for i in range(mealDay-1):
                        var = breakfast_recommendation('KAHVALTILIK TARİFLERİ')
                        
                        popped =retlist.pop(0)
                        list4=ingredient_based_recommendation_recipe(popped)
                        list4 = list4.tolist()
                        list4.pop(0)
                        list4.pop(0)
                        pop1 = list4.pop(0)
                        pop2 = list4.pop(0)
                        
                        data =  { 
                                 'Day' : daycount,
                        'Lunch': pop1,
                        'Dinner': pop2
                        }
                        
                        result = firebase.post('/UserMenus/'+userKey+'/',data)
                        daycount +=1
                
                print(pop1 + " xd" + pop2)
                
            else:
                return(ingredient_based_recommendation_recipe(choice[0]))
                    
        
        return "fuck"

    def post(self):
    # Write method to write data to the CSV file
        return "this is a recommendation post req"
    

class RecommendationOneMeal(Resource):
    # Write method to fetch data from the CSV file
    def get(self):
        userKey = request.args.get("UserKey")
        userPreferences= request.args.get("UserPref")
        mealSelection = int(request.args.get("MealSelect"))
        homeIngres = int(request.args.get("HomeIngredients"))
        ingredientsHome = get_user_cellar_from_firebase(userKey)
        ingredientsHome += ", " + get_user_fav_ingres_from_firebase(userKey)
        recipesliked = get_user_fav_recipes_from_firebase(userKey)
        choice = random.choices(recipesliked)
        
        print(mealSelection)
        if(mealSelection == 0):
            var = breakfast_recommendation('KAHVALTILIK TARİFLERİ')
            return var
        
        if(mealSelection == 1):
            if homeIngres ==1:
                print("Home")
                return(ingredient_based_recommendation(ingredientsHome))
            else:
                return(ingredient_based_recommendation_recipe(choice[0]))
            
        if(mealSelection == 2):
            if homeIngres ==1:
                print("Home")
                return(ingredient_based_recommendation(ingredientsHome))
            else:
                return(ingredient_based_recommendation_recipe(choice[0]))
        
        return "fuck"

    def post(self):
    # Write method to write data to the CSV file
        return "this is a recommendation post req"    


api.add_resource(Hello, '/hello')
api.add_resource(Recommendation, '/recommendation')
api.add_resource(RecommendationLive, '/recommendalive')
api.add_resource(RecommendationOneMeal, '/recommendonemeal')


if __name__ == '__main__':
    app.run()  # run our Flask app
    
    