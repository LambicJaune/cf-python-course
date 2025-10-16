import pickle

def calc_difficulty(cooking_time, ingredients):

            if cooking_time < 10 and len(ingredients) < 4:
                return "Easy"
            elif cooking_time < 10 and len(ingredients) >= 4:
                return "Medium"
            elif cooking_time >= 10 and len(ingredients) < 4:
                return "Intermediate"
            else:
                return "Hard"

def take_recipe():
    while True:
        name = input("Enter the recipe name: ").strip()
        if name == "":
            print("Recipe name cannot be empty. Please try again.")
        else:
            break

    while True:
        cooking_time = input("Enter the cooking time (in minutes): ").strip()
        if not cooking_time.isdigit() or int(cooking_time) <= 0:
            print("Cooking time must be a positive integer. Please try again.")
        else:
            cooking_time = int(cooking_time)
            break

    while True:
        ingredients = input("Enter the ingredients (separated by commas): ").strip()
        if ingredients == "":
            print("Ingredients cannot be empty. Please try again.")
        else:
            #nornalize ingredients by stripping spaces and capitalizing
            ingredients = [i.strip().capitalize() for i in ingredients.split(",")]
            break

    difficulty = calc_difficulty(cooking_time, ingredients)
    
    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients,
        "difficulty": difficulty
    }
    return recipe

my_file = str(input("Enter a filename: "))

data = {"recipes_list": [], "all_ingredients": []}

try:
    file = open(my_file, 'rb')
    data = pickle.load(file)
    if not isinstance(data, dict) or "recipes_list" not in data or "all_ingredients" not in data:
        print("File content is not in the expected format. Initializing new data structure.")
        data = {"recipes_list": [], "all_ingredients": []}

except FileNotFoundError:
    print("File not found.")
    data = {"recipes_list": [], "all_ingredients": []}

except:
    print(f"An error occurred while reading the file {my_file}. Initializing new data structure.")
    data = {"recipes_list": [], "all_ingredients": []}

else:
    file.close()

finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

n = input("Enter the number of recipes you would like to enter: ")

for i in range(int(n)):
    recipe = take_recipe()
    recipes_list.append(recipe)

    for ingredient in recipe["ingredients"]:
        # Normalizes ingredients  by removing spaces and capitalizing in the ingredients list
        ingredient_uniformed = ingredient.strip().capitalize()
        if ingredient_uniformed not in all_ingredients:
            all_ingredients.append(ingredient_uniformed)

data["recipes_list"] = recipes_list

data["all_ingredients"] = all_ingredients

with open(my_file, 'wb') as file:
    pickle.dump(data, file)