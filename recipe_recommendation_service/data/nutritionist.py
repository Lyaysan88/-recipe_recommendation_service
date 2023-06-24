import recipes
import pandas as pd
print("Пример ввода продуктов: Rice, Tomato, Beef")
list_of_ingredients = input("Введите список ингредиентов на английском с большой буквы через запятую: ")
list_of_ing = list_of_ingredients.split(",")
list_of_ing = [x.strip(' ') for x in list_of_ing]
df = pd.read_csv('data2/recipes.csv')
groceries = df.columns[2:]
if len(list_of_ing) <= 1:
    print("Слишком мало продуктов. Введите 2 продукта и более")
elif 1 < len(list_of_ing) <= 5:
    a = 0
    for i in list_of_ing:
        if i not in list(groceries):
            print("Таких ингридиентов нет в нашей базе:", i)
        else: a = a + 1
    if a < len(list_of_ing) :
        print("Попробуйте выбрать что-нибудь из списка:", list(groceries))
    if a == len(list_of_ing) :
        recipe = recipes.Forecast(list_of_ingredients)
        recipe.preprocess()
        rating_cat, text = recipe.predict_rating_category()
        print(' ')
        print("I. НАШ ПРОГНОЗ")
        print(' ')
        print(text)
        print(' ')
        nutrition = recipes.NutritionFacts(list_of_ingredients)
        facts = nutrition.retrieve()
        print("II. ПИЩЕВАЯ ЦЕННОСТЬ")
        for n in list_of_ing:
            print(' ')
            print(n)
            print(' ')
            for nn in range(len(facts)):
                if facts['food_product'][nn] == n:
                    print(facts['nutrition'][nn],' - ',facts['value'][nn],'% of Daily Value')
        similarrecipe = recipes.SimilarRecipes(list_of_ingredients)
        similarrecipe.find_all()
        text_with_recipes = similarrecipe.top_similar()
        print(' ')
        print("III. ТОП-3 ПОХОЖИХ РЕЦЕПТА:")
        print(' ')
        print('- ',text_with_recipes['Title'][0],', рейтинг: ',text_with_recipes['Rating'][0],', URL: ',text_with_recipes['URL'][0])
        print('- ',text_with_recipes['Title'][1],', рейтинг: ',text_with_recipes['Rating'][1],', URL: ',text_with_recipes['URL'][1])
        print('- ',text_with_recipes['Title'][2],', рейтинг: ',text_with_recipes['Rating'][2],', URL: ',text_with_recipes['URL'][2])
        dinner_name,dinner_food,dinner_url,dinner_rating,dinner_nutrition,lunch_name, lunch_food, lunch_url, lunch_rating, lunch_nutrition,breakfast_name, breakfast_food, breakfast_url, breakfast_rating, breakfast_nutrition = similarrecipe.menu_for_day()
        select_ = input("Предложить меню на день Yes / No : ")
        if select_ == 'No':
            print('Пока!')
        elif select_ == 'Yes':
            print(' ')
            print('МЕНЮ НА ДЕНЬ')
            print(' ')
            print('ЗАВТРАК')
            print('---------------------')
            print(breakfast_name,' (рейтинг: ',breakfast_rating,')')
            print(' ')
            print('Ингридиенты:')
            for i in breakfast_food:
                print('-',i)
            print(' ')
            print('Nutrients:')
            print(' ')
            for j in range(len(breakfast_nutrition)):
                print('-',breakfast_nutrition['nutrition'][j],': ',breakfast_nutrition['value'][j],'%')
            print('URL: ', breakfast_url)
            print(' ')
            print('ОБЕД')
            print('---------------------')
            print(lunch_name, ' (рейтинг: ', lunch_rating, ')')
            print(' ')
            print('Ингридиенты:')
            for i in lunch_food:
                print('-', i)
            print(' ')
            print('Nutrients:')
            print(' ')
            for j in range(len(lunch_nutrition)):
                print('-', lunch_nutrition['nutrition'][j], ': ', lunch_nutrition['value'][j], '%')
            print('URL: ', lunch_url)
            print(' ')
            print('УЖИН')
            print('---------------------')
            print(dinner_name, ' (рейтинг: ', dinner_rating, ')')
            print(' ')
            print('Ингридиенты:')
            for i in dinner_food:
                print('-', i)
            print(' ')
            print('Nutrients:')
            print(' ')
            for j in range(len(dinner_nutrition)):
                print('-', dinner_nutrition['nutrition'][j], ': ', dinner_nutrition['value'][j], '%')
            print('URL: ', dinner_url)
            print(' ')
            print('ДО СКОРЫХ ВСТРЕЧ!')
        else :
            print('Введена неверная команда :(')
else: print("Похожих рецептов не найдено")