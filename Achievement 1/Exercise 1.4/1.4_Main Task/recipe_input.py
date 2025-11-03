import pickle

"""Calculates the difficulty level of a recipe based on cooking time and number of ingredients."""
def calc_difficulty(cooking_time, ingredients):

            if cooking_time < 10 and len(ingredients) < 4:
                return "Easy"
            elif cooking_time < 10 and len(ingredients) >= 4:
                return "Medium"
            elif cooking_time >= 10 and len(ingredients) < 4:
                return "Intermediate"
            else:
                return "Hard"

"""Collects user input for a recipe, validates it, and returns a structured recipe dictionary."""
def take_recipe():
    while True:
        name = input("Enter the recipe name: ").strip()
        if name == "":
            print("Recipe name cannot be empty. Please try again.")
        else:
            break

    # Validates that cooking time is a positive integer.
    while True:
        cooking_time = input("Enter the cooking time (in minutes): ").strip()
        if not cooking_time.isdigit() or int(cooking_time) <= 0:
            print("Cooking time must be a positive integer. Please try again.")
        else:
            cooking_time = int(cooking_time)
            break

    # Ensures that ingredients input is not empty and processes it into a list.
    while True:
        ingredients = input("Enter the ingredients (separated by commas): ").strip()
        if ingredients == "":
            print("Ingredients cannot be empty. Please try again.")
        else:
            # Normalizes ingredients by stripping spaces and capitalizing
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

# Main program logic to handle file operations and recipe input.
my_file = str(input("Enter a filename: "))

# Attempts to open the specified file and load existing data; 
# initializes new data structure if file is not found or content is invalid.
data = {"recipes_list": [], "all_ingredients": []}

# Attempts to open the specified file and load existing data; 
# initializes new data structure if file is not found or content is invalid.
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

# Regardless of file operation outcome, ensure recipes_list and all_ingredients are initialized.
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]

# Prompts user for the number of recipes to enter and collects each recipe using take_recipe function.
# Updates the all_ingredients list to include any new ingredients from the entered recipes.
n = input("Enter the number of recipes you would like to enter: ")

for i in range(int(n)):
    recipe = take_recipe()
    recipes_list.append(recipe)

    for ingredient in recipe["ingredients"]:
        # Normalizes ingredients  by removing spaces and capitalizing in the ingredients list
        ingredient_uniformed = ingredient.strip().capitalize()
        if ingredient_uniformed not in all_ingredients:
            all_ingredients.append(ingredient_uniformed)

# Saves the updated data back to the specified file.
data["recipes_list"] = recipes_list

data["all_ingredients"] = all_ingredients

with open(my_file, 'wb') as file:
    pickle.dump(data, file)