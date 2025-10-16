import pickle

"""Makes sure the recipe argument is a dictionary and displays its details in a formatted way."""
def display_recipe(recipe: dict):
    print(f"Recipe Name: {recipe['name']}")
    print(f"Cooking Time (min): {recipe['cooking_time']}")
    print(f"Ingredients: {', '.join(recipe['ingredients'])}")
    print(f"Difficulty: {recipe['difficulty']}")
    print("-" * 30)

"""Allows the user to search for recipes by selecting an ingredient from an ordered displayed list.
prompts the user to select an ingredient by number, and then displays matching recipes."""
# Index starts at 1 for display only; internally, list indexing starts at 0.
def search_ingredient(data: dict):
    for index, ingredient in enumerate(data["all_ingredients"], start=1):
        print(f"{index}. {ingredient}")

    # Prompts user to select an ingredient by number, validates input, and displays matching recipes.
    # While loop continues until valid input is received.
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

    # Once validation is complete, searches through recipes and displays those containing the selected ingredient.
    for recipe in data["recipes_list"]:
        if ingredient_searched in recipe["ingredients"]:
            display_recipe(recipe)
            found = True
    if not found:
        print(f"No recipes found containing '{ingredient_searched}'.")

    return ingredient_searched

# Main program loop to prompt for filename, handle file operations, and initiate ingredient search.
# Continues until a valid file is provided and processed.
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

    # If file is successfully opened and data is valid, proceed to ingredient search from the data dictionary.
    else:
        search_ingredient(data)
        break