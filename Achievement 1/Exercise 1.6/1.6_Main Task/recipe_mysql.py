from dataclasses import fields
import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='cf-python',
    passwd='password')

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")
cursor.execute("USE task_database")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS recipes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(50) NOT NULL,
        ingredients VARCHAR(255) NOT NULL,
        cooking_time INT NOT NULL,
        difficulty VARCHAR(20) NOT NULL
    )
""")

def calculate_difficulty(cooking_time, ingredients):
        """Function to calculate difficulty based on cooking time and number of ingredients"""
        # Placed here to allow reuse across multiple functions
        if cooking_time < 10 and len(ingredients) < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and len(ingredients) >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and len(ingredients) < 4:
            difficulty = "Intermediate"
        else:
            difficulty = "Hard"
        return difficulty
       
def create_recipe(conn, cursor):
    """Create a new recipe in the database"""
    # calculate_difficulty() is called to calculate difficulty level automatically on new recipe creation
    name = input("Enter recipe name: ")
    cooking_time = int(input("Enter cooking time (in minutes): "))
    ingredients = input("Enter ingredients (comma separated): ").split(',')
    difficulty = calculate_difficulty(cooking_time, ingredients)


    sql = "INSERT INTO recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)"
    val = (name, ', '.join(ingredients), cooking_time, difficulty)
    cursor.execute(sql, val)
    conn.commit()
    print(f"Recipe '{name}' added successfully.")

def search_recipe(conn, cursor):
    """Search for recipes by ingredient"""
    sql = "SELECT ingredients FROM recipes"
    cursor.execute(sql)
    results = cursor.fetchall()
    
    all_ingredients = set()
    # Collect all unique ingredients from the recipes
    for row in results:
        recipe_ingredients = [i.strip().lower() for i in row[0].split(',')]
        all_ingredients.update(recipe_ingredients)
    # Sort ingredients for better display, as sets are unordered by default
    all_ingredients = list(all_ingredients)
    all_ingredients.sort()
    # Create a numbered list of ingredients for user selection
    search_ingredients = {i+1: ing for i, ing in enumerate(all_ingredients)}
    print("Available ingredients to search: ")
    for num, ing in search_ingredients.items():
        print(f"  {num}. {ing}")

    user_input = input("\nEnter a number in the ingredient list to search for: ")
    if not user_input.isdigit():
        print("Invalid input. Please enter a number.")
        return

    ingredients_num = int(user_input)

    if ingredients_num not in search_ingredients:
        print(f"Invalid selection. Please choose a number between 1 and {len(search_ingredients)}.")
        return
    # Map user input number to the corresponding ingredient
    search_ingredient = search_ingredients.get(int(user_input), None)
    if not search_ingredient:
        print("Invalid selection.")
        return

    sql = "SELECT * FROM recipes WHERE ingredients LIKE %s"
    val = ('%' + search_ingredient + '%',)
    cursor.execute(sql, val)
    results = cursor.fetchall()
    if results:
        print(f"\nRecipes containing '{search_ingredient}':")
        for recipe in results:
            print(f"\nID: {recipe[0]}, Name: {recipe[1]}, Ingredients: {recipe[2]}, Cooking Time: {recipe[3]} mins, Difficulty: {recipe[4]}")
    else:
        print("No recipes found with that ingredient.")

def update_recipe(conn, cursor):
    """Update an existing recipe in the database"""
    sql = "SELECT * FROM recipes"
    cursor.execute(sql)
    results = cursor.fetchall()

    for row in results:
        print("\nCurrent Recipes: ")
        print(f"\nID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Ingredients: {row[2]}")
        print(f"Cooking Time: {row[3]} mins")
        print(f"Difficulty: {row[4]}")

    chosen_recipe_id = input("\nEnter the ID of the recipe you want to update: ")
    if not chosen_recipe_id.isdigit():
        print("Invalid input. Please enter a numeric recipe ID.")
        return
    recipe_id = int(chosen_recipe_id)

    column_to_modify = input("Enter the field you want to update (name, ingredients, cooking_time): ").lower()
    if column_to_modify not in ['name', 'ingredients', 'cooking_time']:
        print("Invalid field. Please choose from 'name', 'ingredients', or 'cooking_time'.")
        return

    # initialize new_value variable with a placeholder
    new_value = None

    if column_to_modify == 'name':
        new_value = input("Enter the new name: ")
    elif column_to_modify == 'ingredients':
        new_value = input("Enter the new ingredients (separated by commas): ")
    elif column_to_modify == 'cooking_time':
        new_value = input("Enter the new cooking time (in minutes): ")
        if not new_value.isdigit():
            print("Invalid input. Please enter a numeric cooking time.")
            return
        new_value = int(new_value)

    sql = f"UPDATE recipes SET {column_to_modify} = %s WHERE id = %s"
    val = (new_value, recipe_id)
    cursor.execute(sql, val)
    if column_to_modify in ['ingredients', 'cooking_time']:
        cursor.execute("SELECT ingredients, cooking_time FROM recipes WHERE id = %s", (recipe_id,))
        recipe = cursor.fetchone()
        ingredients = [i.strip() for i in recipe[0].split(',')]
        cooking_time = recipe[1]
        new_difficulty = calculate_difficulty(cooking_time, ingredients)
        cursor.execute("UPDATE recipes SET difficulty = %s WHERE id = %s", (new_difficulty, recipe_id))
    conn.commit()
    print("Recipe updated successfully.")

def delete_recipe(conn, cursor):
    """Delete a recipe from the database"""
    sql = "SELECT * FROM recipes"
    cursor.execute(sql)
    results = cursor.fetchall()

    for row in results:
        print(f"ID: {row[0]}")
        print(f"Name: {row[1]}")
        print(f"Ingredients: {row[2]}")
        print(f"Cooking Time: {row[3]} mins")
        print(f"Difficulty: {row[4]}")

    chosen_recipe_id = input("\nEnter the ID of the recipe you want to delete: ")
    if not chosen_recipe_id.isdigit():
        print("Invalid input. Please enter a numeric recipe ID.")
        return
    recipe_id = int(chosen_recipe_id)

    sql = "DELETE FROM recipes WHERE id = %s"
    val = (recipe_id,)
    cursor.execute(sql, val)
    conn.commit()
    print("Recipe deleted successfully.")


def main_menu(conn, cursor):
    """Display the main menu and handle user choices"""
    choice = ''    
    while(choice != 'quit'):
        print("\nMain Menu")
        print("======================")
        print("Pick a choice:")
        print("         1. Create a new recipe")
        print("         2. Search for a recipe by ingredient")
        print("         3. Update an existing recipe")
        print("         4. Delete a recipe")
        print("         5. Quit")
        choice = input("Your choice: ").lower()

        if choice == '1':
            create_recipe(conn, cursor)
        elif choice == '2':
            search_recipe(conn, cursor)
        elif choice == '3':
            update_recipe(conn, cursor)
        elif choice == '4':
            delete_recipe(conn, cursor)
        elif choice == '5' or choice == 'quit':
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please try again.")

main_menu(conn, cursor)

cursor.close()
conn.close()