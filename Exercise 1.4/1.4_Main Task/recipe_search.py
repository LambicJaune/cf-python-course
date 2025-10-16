import pickle

def display_recipe(recipe: dict):
    print(f"Recipe Name: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {recipe['difficulty']}")
    print("-" * 30)

def search_ingredient(data: dict):
    for index, ingredient in enumerate(data["all_ingredients"], start=1):
        print(f"{index}. {ingredient}")

    while True:
        try:
            choice = int(input("Select an ingredient by number: "))
            if choice < 1 or choice > len(data["all_ingredients"]):
                print("Invalid choice. Please try again by entering a number in the list.")
                continue
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue
        else:
            ingredient_searched = data["all_ingredients"][choice - 1]
            print(f"You selected: {ingredient_searched}")
            break

    found = False

    for recipe in data["recipes_list"]:
        if ingredient_searched in recipe["ingredients"]:
            display_recipe(recipe)
            found = True
    if not found:
        print(f"No recipes found containing '{ingredient_searched}'.")

    return ingredient_searched

while True:
    filename = input("\nEnter the name of the file that contains your recipe data: ").strip()

    try:
        with open(filename, 'rb') as file:
            data = pickle.load(file)
            if not isinstance(data, dict) or "recipes_list" not in data or "all_ingredients" not in data:
                print("File content is not in the expected format.")
                continue

    except FileNotFoundError:
        print("File not found. Please check the filename and try again.")
        continue

    else:
        search_ingredient(data)
        break