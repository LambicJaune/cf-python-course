recipes_list = []
ingredients_list = []

def take_recipe():

    while True:
        
        name = input("Enter the recipe name: ").strip()
        if name == "":
            print("Recipe name cannot be empty. Please try again.")
        else:
            break

    while True:

        cooking_time = input("Enter the cooking time (in minutes): ").strip()
        if cooking_time == "":
            print("Cooking time cannot be empty. Please try again.")
            continue
        if not cooking_time.isdigit():
            print("Cooking time must be a number. Please try again.")
            continue
        break

    while True:
        ingredients = input("Enter the ingredients (separated by commas): ").strip()
        if ingredients == "":
            print("Ingredients cannot be empty. Please try again.")
        else:
            #nornalize ingredients by stripping spaces and capitalizing inside the recipes
            ingredients = [i.strip().capitalize() for i in ingredients.split(",")]
            break

    recipe = {
        "name": name,
        "cooking_time": cooking_time,
        "ingredients": ingredients
    }

    return recipe

n = input("Enter the number of recipes you would like to enter: ")

for i in range(int(n)):
    recipe = take_recipe()

    for ingredient in recipe["ingredients"]:
        # Normalizes ingredients  by removing spaces and capitalizing in the ingredients list
        ingredient_uniformed = ingredient.strip().capitalize()
        if ingredient_uniformed not in ingredients_list:
            ingredients_list.append(ingredient_uniformed)

    recipes_list.append(recipe)

for recipe in recipes_list:
    if int(recipe["cooking_time"]) < 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Easy"
    elif int(recipe["cooking_time"]) < 10 and len(recipe["ingredients"]) >= 4:
        recipe["difficulty"] = "Medium"
    elif int(recipe["cooking_time"]) >= 10 and len(recipe["ingredients"]) < 4:
        recipe["difficulty"] = "Intermediate"
    else:
        recipe["difficulty"] = "Hard"

for recipe in recipes_list:
    print(
        f"Recipe: {recipe['name']}\n"
          f"Cooking Time (min): {recipe['cooking_time']}\n"
          f"Ingredients:\n" +
          "\n".join(f"- {i.strip()}" for i in recipe["ingredients"]) +
          f"\nDifficulty: {recipe['difficulty']}\n"
          )
    
print("Ingredients Available Across All Recipes")
print("----------------------------------------")

for ingredient in ingredients_list:
    print(f"- {ingredient.strip()}")
