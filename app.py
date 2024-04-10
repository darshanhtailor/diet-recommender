from flask import Flask, request, jsonify
import pandas as pd
from pymongo import MongoClient
from model import recommend

app = Flask(__name__)

def fetch_recipes():
    try:
        df = pd.read_csv('./indian_recipes.csv')
        columns=['RecipeId','Name','TotalTime','RecipeIngredientParts','Calories','FatContent','SaturatedFatContent','CholesterolContent','SodiumContent','CarbohydrateContent','FiberContent','SugarContent','ProteinContent','RecipeInstructions', 'Keywords']
        df=df[columns]
        return df

    except Exception as e:
        print("An error occurred:", e)
        return None


@app.route('/meals', methods=['POST'])
def get_meals():
    try:
        df = fetch_recipes()
        if 0:

            name = request.args.get('name')

            for meal in self.meals_calories_perc:
                meal_calories=self.meals_calories_perc[meal]*total_calories
                if meal=='breakfast':        
                    recommended_nutrition = [meal_calories,rnd(10,30),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,10),rnd(0,10),rnd(30,100)]
                elif meal=='launch':
                    recommended_nutrition = [meal_calories,rnd(20,40),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,20),rnd(0,10),rnd(50,175)]
                elif meal=='dinner':
                    recommended_nutrition = [meal_calories,rnd(20,40),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,20),rnd(0,10),rnd(50,175)] 
                else:
                    recommended_nutrition = [meal_calories,rnd(10,30),rnd(0,4),rnd(0,30),rnd(0,400),rnd(40,75),rnd(4,10),rnd(0,10),rnd(30,100)]
                pass

        if df is not None:
            max_list = [float('inf'), float('inf'), 13, 300, 2300, float('inf'), float('inf'), 40, float('inf')]
            # ingredient_filter = ['cottage cheese']
            content = df.iloc[0:1, 4:13]
            _input = content.to_numpy()

            rec = recommend(df, max_list, _input=_input)
            return jsonify(rec.to_dict(orient='records'))
        else:
            return jsonify({'error': 'failed to fetch recipes'})

    except Exception as e:
        return jsonify({'error': str(e)})


@app.route('/')
def hello_world():
    return 'diet recommendation by fitzing'

if __name__ == '__main__':
    app.run(debug=True, port=5001)