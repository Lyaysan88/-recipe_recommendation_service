import pandas as pd
import numpy as np
import joblib
import warnings

warnings.filterwarnings('ignore')
import random

class Forecast:

    def __init__(self, list_of_ingredients):
        self.list_of_ingredients = list_of_ingredients
        self.list_of_ingredients = self.list_of_ingredients.split(",")
        self.list_of_ingredients = [x.strip(' ') for x in self.list_of_ingredients]

    def preprocess(self):
        df = pd.read_csv('data2/recipes.csv')
        groceries = df.columns[2:339]
        vector = pd.DataFrame(data=np.zeros((1, len(groceries))), columns=groceries)
        for i in list(groceries):
            if i in self.list_of_ingredients:
                vector[i] = 1.0
        self.vector = vector
        return self.vector

    def predict_rating_category(self):
        model = joblib.load('data2/Best_RandomForestClassifier.joblib')
        rating_cat = model.predict(self.vector)
        if rating_cat == 'great':
            text = 'great. Хороший выбор продуктов!'
        if rating_cat == 'soso':
            text = 'so-so. Пересмотрим что-то в списке продуктов?'
        if rating_cat == 'bad':
            text = 'bad. Не советуем готовить с таким набором продуктов.'
        rating_cat = rating_cat
        return rating_cat, text

class NutritionFacts:

    def __init__(self, list_of_ingredients):
        self.list_of_ingredients = list_of_ingredients
        self.list_of_ingredients = self.list_of_ingredients.split(",")
        self.list_of_ingredients = [x.strip(' ') for x in self.list_of_ingredients]

    def retrieve(self):
        df = pd.read_csv('data2/nutrition.csv')
        for i in self.list_of_ingredients:
            if i == self.list_of_ingredients[0]:
                nutr = df.loc[df['food_product'] == i]
                df_nutr = nutr
            else:
                nutr = df.loc[df['food_product'] == i]
                df_nutr = pd.concat([df_nutr, nutr])
        df_nutr.reset_index(drop=True, inplace=True)
        for x in range(len(df_nutr)):
            df_nutr['value'][x] = round(df_nutr['value'][x] * 100, 0)
            df_nutr['nutrition'][x] = df_nutr['nutrition'][x].split(',')[0]

        df_nutr = df_nutr.loc[df_nutr['value'] > 0]
        df_nutr = df_nutr.sort_values(by=['food_product', 'value'], ascending=False)
        df_nutr.reset_index(drop=True, inplace=True)
        self.facts = df_nutr
        return self.facts


class SimilarRecipes:

    def __init__(self, list_of_ingredients):
        self.list_of_ingredients = list_of_ingredients
        self.list_of_ingredients = self.list_of_ingredients.split(",")
        self.list_of_ingredients = [x.strip(' ') for x in self.list_of_ingredients]

    def find_all(self):
        df = pd.read_csv('data2/recipes.csv')
        for i in self.list_of_ingredients:
            if i == self.list_of_ingredients[0]:
                df_rec = df.loc[df[i] == 1]
                df_recipes = df_rec
            else:
                df_rec = df.loc[df[i] == 1]
                df_recipes = pd.concat([df_recipes, df_rec])
        df_recipes = df_recipes.drop_duplicates(keep='first')
        df_recipes.reset_index(drop=True, inplace=True)
        df_recipes['ing'] = df_recipes['val']
        df_recipes['ing_n'] = df_recipes['val']
        for x in range(len(df_recipes)):
            df_recipes['ing'][x] = 0
            for y in self.list_of_ingredients:
                df_recipes['ing'][x] = df_recipes['ing'][x] + df_recipes[y][x]
            df_recipes['ing_n'][x] = df_recipes['val'][x] - df_recipes['ing'][x]
        df_recipes = df_recipes.sort_values(by=['ing', 'ing_n'], ascending=[False, True])
        self.indexes = df_recipes
        return self.indexes

    def top_similar(self):
        text_with_recipes = self.indexes
        text_with_recipes = text_with_recipes.loc[text_with_recipes['ing_n'] <= 5]
        text_with_recipes.reset_index(drop=True, inplace=True)
        return text_with_recipes

    def menu_for_day(self):
        df = pd.read_csv('data2/recipes.csv')
        df_breakfast = df.loc[df['meal'] == 'breakfast']
        df_breakfast = df_breakfast.loc[df_breakfast['class'] == 'great']
        df_breakfast = df_breakfast.loc[df_breakfast['val'] >= 3]
        breakfast = df_breakfast.loc[random.choice(list(df_breakfast.index))]
        cc = breakfast['Title']
        df_breakfast = df_breakfast.loc[df_breakfast['Title'] == cc]
        df_breakfast.reset_index(drop=True, inplace=True)
        groceries = df_breakfast.columns[6:]
        vv = []
        for a in groceries:
            if df_breakfast[a][0] == 1:
                vv.append(a)
        df2 = pd.read_csv('data2/nutrition.csv')
        for i in vv:
            if i == vv[0]:
                nutr = df2.loc[df2['food_product'] == i]
                df_nutr = nutr
            else:
                nutr = df2.loc[df2['food_product'] == i]
                df_nutr = pd.concat([df_nutr, nutr])
        table_breakfast = pd.pivot_table(df_nutr, values='value', index=['nutrition'], aggfunc=np.sum)
        table_breakfast.reset_index(drop=False, inplace=True)
        for i in range(len(table_breakfast)):
            table_breakfast['value'][i] = round(table_breakfast['value'][i] * 100, 0)
            table_breakfast['nutrition'][i] = table_breakfast['nutrition'][i].split(',')[0]
        table_breakfast = table_breakfast.sort_values(by=['value'], ascending=[False])
        table_breakfast.reset_index(drop=True, inplace=True)
        breakfast_name = cc
        breakfast_food = vv
        breakfast_url = df_breakfast['URL'][0]
        breakfast_rating = df_breakfast['Rating'][0]
        breakfast_nutrition = table_breakfast
        # -----------------------------------------------------------------------
        df_lunch = df.loc[df['meal'] == 'lunch']
        df_lunch = df_lunch.loc[df_lunch['class'] == 'great']
        df_lunch = df_lunch.loc[df_lunch['val'] >= 3]
        lunch = df_lunch.loc[random.choice(list(df_lunch.index))]
        cc = lunch['Title']
        df_lunch = df_lunch.loc[df_lunch['Title'] == cc]
        df_lunch.reset_index(drop=True, inplace=True)
        groceries = df_lunch.columns[2:339]
        vv = []
        for a in groceries:
            if df_lunch[a][0] == 1:
                vv.append(a)
        for i in vv:
            if i == vv[0]:
                nutr = df2.loc[df2['food_product'] == i]
                df_nutr = nutr
            else:
                nutr = df2.loc[df2['food_product'] == i]
                df_nutr = pd.concat([df_nutr, nutr])
        table_lunch = pd.pivot_table(df_nutr, values='value', index=['nutrition'], aggfunc=np.sum)
        table_lunch.reset_index(drop=False, inplace=True)
        for i in range(len(table_lunch)):
            table_lunch['value'][i] = round(table_lunch['value'][i] * 100, 0)
            table_lunch['nutrition'][i] = table_lunch['nutrition'][i].split(',')[0]
        table_lunch = table_lunch.sort_values(by=['value'], ascending=[False])
        table_lunch.reset_index(drop=True, inplace=True)
        lunch_name = cc
        lunch_food = vv
        lunch_url = df_lunch['URL'][0]
        lunch_rating = df_lunch['Rating'][0]
        lunch_nutrition = table_lunch
        # -----------------------------------------------------------------------
        df_dinner = df.loc[df['meal'] == 'dinner']
        df_dinner = df_dinner.loc[df_dinner['class'] == 'great']
        df_dinner = df_dinner.loc[df_dinner['val'] >= 3]
        dinner = df_dinner.loc[random.choice(list(df_dinner.index))]
        cc = dinner['Title']
        df_dinner = df_dinner.loc[df_dinner['Title'] == cc]
        df_dinner.reset_index(drop=True, inplace=True)
        groceries = df_dinner.columns[2:339]
        vv = []
        for a in groceries:
            if df_dinner[a][0] == 1:
                vv.append(a)
        for i in vv:
            if i == vv[0]:
                nutr = df2.loc[df2['food_product'] == i]
                df_nutr = nutr
            else:
                nutr = df2.loc[df2['food_product'] == i]
                df_nutr = pd.concat([df_nutr, nutr])
        table_dinner = pd.pivot_table(df_nutr, values='value', index=['nutrition'], aggfunc=np.sum)
        table_dinner.reset_index(drop=False, inplace=True)
        for i in range(len(table_dinner)):
            table_dinner['value'][i] = round(table_dinner['value'][i] * 100, 0)
            table_dinner['nutrition'][i] = table_dinner['nutrition'][i].split(',')[0]
        table_dinner = table_dinner.sort_values(by=['value'], ascending=[False])
        table_dinner.reset_index(drop=True, inplace=True)
        dinner_name = cc
        dinner_food = vv
        dinner_url = df_dinner['URL'][0]
        dinner_rating = df_dinner['Rating'][0]
        dinner_nutrition = table_dinner
        return dinner_name, dinner_food, dinner_url, dinner_rating, dinner_nutrition, lunch_name, lunch_food, lunch_url, lunch_rating, lunch_nutrition, breakfast_name, breakfast_food, breakfast_url, breakfast_rating, breakfast_nutrition


