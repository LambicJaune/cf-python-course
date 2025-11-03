from sqlalchemy import create_engine, Column, Integer, String, or_
from sqlalchemy.orm import sessionmaker, declarative_base

engine = create_engine("mysql+pymysql://cf-python:password@localhost/task_database")

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    def __repr__(self):
        """Return a short string representation of the recipe."""
        return f"<Recipe ID: {self.id} - {self.name.title()} - Difficulty: {self.difficulty}>"
    
    def __str__(self):
        """Return a formatted string representation of the recipe details."""
        border = "=" * 45
        ingredients_list = [i.strip().title() for i in self.ingredients.split(",")]
        ingredients_formatted = "\n\t- " + "\n\t- ".join(ingredients_list)
        label_width = 15
        return (
            f"🍽️\u00A0Recipe Details\u00A0🍽️\n"
            f"{border}\n"
            f"🧾  {'Recipe ID:':<{label_width}} {self.id}\n"
            f"🏷️  {'Name:':<{label_width}} {self.name}\n"
            f"🕒  {'Cooking Time:':<{label_width}} {self.cooking_time} minutes\n"
            f"🥣  {'Ingredients:':<{label_width}}{ingredients_formatted}\n"
            f"💪  {'Difficulty:':<{label_width}} {self.difficulty}\n"
            f"{border}"
        )

    def calculate_difficulty(self, cooking_time, ingredients):
            """Function to calculate difficulty based on cooking time and number of ingredients"""
            if cooking_time < 10 and len(ingredients) < 4:
                difficulty = "Easy"
            elif cooking_time < 10 and len(ingredients) >= 4:
                difficulty = "Medium"
            elif cooking_time >= 10 and len(ingredients) < 4:
                difficulty = "Intermediate"
            else:
                difficulty = "Hard"

            self.difficulty = difficulty
            return self.difficulty

    def return_ingredients_as_list(self):
        """Return a list of ingredients for the recipe"""
        if not isinstance(self.ingredients, str):
            # Ensure ingredients is a string
            raise TypeError(f"Expected 'ingredients' to be a string, got {type(self.ingredients).__name__}")
        if not self.ingredients:
        # Check for empty ingredients
            return []
        ingredients_list = [ingredient.strip() for ingredient in self.ingredients.split(',')]
        return ingredients_list

def create_recipe(session):
    """Create a new recipe in the database, with input validation"""
    while True:
        name = input("Enter recipe name: ").strip()
        if not name:
            print("Recipe name cannot be empty.")
            continue
        elif name.isnumeric():
            print("Recipe name cannot be only a number.")
            continue
        elif len(name) > 50:
            print("Recipe name cannot exceed 50 characters.")
            continue
        else:
            break
    while True:
        cooking_time = input("Enter cooking time (in minutes): ").strip()
        if not cooking_time.isnumeric():
            print("Cooking time must be a number.")
            continue
        cooking_time = int(cooking_time)
        if cooking_time < 0:
            print("Cooking time cannot be a negative number.")
            continue
        else:
            break
    while True:
        ingredients = []
        num_ingredients = input("Enter number of ingredients: ").strip()
        if not num_ingredients.isnumeric():
            print("Number of ingredients must be a number.")
            continue
        num_ingredients = int(num_ingredients)
        if num_ingredients <= 0:
            print("Number of ingredients must be a positive integer.")
            continue

        for i in range(num_ingredients):
            while True:
                ingredient = input(f"Enter ingredient {i + 1}: ").strip()
                if not ingredient:
                    print("Ingredient cannot be empty, please try again.")
                else:
                    ingredient = " ".join(ingredient.split()).lower()  # Normalize spaces and lowercase
                    ingredients.append(ingredient)
                    break

        ingredients_list = ingredients.copy()  # copy for difficulty calculation as it expects a list

        ingredients_str = ', '.join(ingredients) # join for storage in DB

        if len(ingredients_str) > 255:
            print("Ingredients list cannot exceed 255 characters.")
            continue

        break

    recipe_entry = Recipe(
        name=name,
        ingredients=ingredients_str,
        cooking_time=cooking_time
    )
    recipe_entry.calculate_difficulty(cooking_time, ingredients_list)

    session.add(recipe_entry)
    session.commit()
    print(f"\nRecipe '{name}' added successfully.")
    print(recipe_entry)

def view_all_recipes(session):
    """View all recipes in the database"""
    recipes = session.query(Recipe).all()  
    if not recipes:
        print("No recipes found in the database.")
        return None
    for recipe in recipes:
        print(recipe.__str__())
    return recipes

def search_by_ingredients(session):
    """Search for recipes by ingredient"""
    if not session.query(Recipe).count():
        print("No recipes found in the database.")
        return None
    results = session.query(Recipe.ingredients).all()
    
    all_ingredients = set()
    for row in results:
        # Collect all unique ingredients from the recipes
        recipe_ingredients = [i.strip().lower() for i in row[0].split(',')]
        all_ingredients.update(recipe_ingredients)
    all_ingredients = list(all_ingredients)
    all_ingredients.sort()
    # Sort ingredients for better display, as sets are unordered by default
    search_ingredients = {i+1: ing for i, ing in enumerate(all_ingredients)}
    # Create a numbered list of ingredients for user selection
    print("Available ingredients to search: ")
    for num, ing in search_ingredients.items():
        print(f"  {num}. {ing.capitalize()}")

    user_input = input("\nSelect ingredients by number (separated by spaces): ")
    if not user_input:
        print("Invalid input. Please enter at least one valid number.")
        return

    ingredient_numbers = [int(num.strip()) for num in user_input.split() if num.strip().isdigit()]
    if not ingredient_numbers:
        print("Invalid input. Please enter at least one valid number.")
        return

    for num in ingredient_numbers:
        if num not in search_ingredients:
            print(f"Invalid selection. Please choose a number between 1 and {len(search_ingredients)}.")
            return
        
    search_ingredients = sorted(search_ingredients[num] for num in ingredient_numbers)
    # Convert selected numbers to ingredient names and sort them
    search_ingredient_str = ', '.join(search_ingredients)
    # Purely for display purposes

    conditions = []

    for ing in search_ingredients:
        ing = ing.strip().lower()
        conditions.append(Recipe.ingredients.like(f"%{ing}%"))
        # Build conditions for SQLAlchemy query

    if conditions:
        print(f"\nRecipes containing '{search_ingredient_str}':\n")
        for recipe in session.query(Recipe).filter(or_(*conditions)).all():
            print(recipe) # __str__ method called here
    else:
        print("No recipes found with the selected ingredient(s).")

def edit_recipe(session):
    """Update an existing recipe in the database"""
    if session.query(Recipe).count() == 0:
        print("No recipes found in the database.")
        return None

    results = session.query(Recipe.id, Recipe.name).all()
    print("Current Recipes: ")
    for row in results:
        print(f"ID: {row[0]}, Name: {row[1]}")

    recipe_id = input("\nEnter the ID of the recipe you want to update: ").strip()
    if not recipe_id.isdigit():
        print("Invalid input. Please enter a valid recipe ID.")
        return
    recipe_id = int(recipe_id)

    recipe_to_edit = session.query(Recipe).filter_by(id=recipe_id).first()
    if not recipe_to_edit:
        print(f"No recipe found with ID {recipe_id}.")
        return
    
    editable_fields = [
        ('name', recipe_to_edit.name),
        ('cooking_time', recipe_to_edit.cooking_time),
        ('ingredients', recipe_to_edit.ingredients)
    ]

    print("\nCurrent recipe:")
    for i, (field, value) in enumerate(editable_fields, start=1):
        print(f"{i}. {field.capitalize()} (current: {value})")

    selection_input = input("\nSelect fields to update by number (comma-separated): ").strip()
    selected_field_numbers = [num.strip() for num in selection_input.split(',') if num.strip().isdigit()]
    if not selected_field_numbers:
        print("No valid fields selected for update.")
        return
    
    selected_fields = []

    for num in selected_field_numbers:
        index = int(num) - 1
        if 0 <= index < len(editable_fields):
            selected_fields.append(editable_fields[index][0])  # Get field name
        else:
            print(f"Invalid selection: {num}. Skipping.")
            continue
    if not selected_fields:
        print("No valid fields selected for update. Returning to menu")
        return
    
    print("Selected fields for update:")
    for field in selected_fields:
        print(f" - {field.capitalize()}")

    for field in selected_fields:
        new_value = input(f"Enter new value for {field} (leave blank to keep current): ").strip()
        if not new_value:
            print(f"{field.capitalize()} remains unchanged.")
            continue

        if field == "cooking_time":
            if not new_value.isdigit():
                print("Cooking time must be a number.")
                return
            else:
                new_value = int(new_value)
                setattr(recipe_to_edit, field, new_value)
        else:
            if field == "ingredients":
                if len(new_value) > 255:
                    print("Ingredients list cannot exceed 255 characters.")
                    return
                else:
                    # Normalize ingredients formatting
                    ingredients_list = [
                        ingredient.strip().lower() 
                        for ingredient in new_value.split(",") 
                        if ingredient.strip()
                    ]
                    new_value = ", ".join(ingredients_list)
                    setattr(recipe_to_edit, field, new_value)
            else: #field == "name"
                if len(new_value) > 50:
                    print("Recipe name cannot exceed 50 characters.")
                    return
                else:
                    setattr(recipe_to_edit, field, new_value)
            
    # Recalculate difficulty if cooking time or ingredients were updated
    if "cooking_time" in selected_fields or "ingredients" in selected_fields:
        ingredients_list = recipe_to_edit.return_ingredients_as_list()
        recipe_to_edit.calculate_difficulty(recipe_to_edit.cooking_time, ingredients_list)

    session.commit()
    print(f"\nRecipe ID {recipe_id} updated successfully.")
    print(recipe_to_edit)

def delete_recipe(session):
    """Delete a recipe from the database"""
    if session.query(Recipe).count() == 0:
    # Check if the DB is empty
        print("No recipes found in the database.")
        return None

    results = session.query(Recipe.id, Recipe.name).all()
    print("Current Recipes: ")
    for row in results:
        print(f"ID: {row[0]}, Name: {row[1]}")

    chosen_recipe_id = input("\nEnter the ID of the recipe you want to delete: ").strip()
    if not chosen_recipe_id.isdigit():
        print("Invalid input. Please enter a numeric recipe ID from the list above.")
        return
    recipe_id = int(chosen_recipe_id)

    recipe_to_delete = session.query(Recipe).filter_by(id=recipe_id).first()
    if not recipe_to_delete:
        print(f"No recipe found with ID {recipe_id}.")
        return
    else:
        print(f"Recipe ID {recipe_id} found: {recipe_to_delete.name}. Are you sure you want to delete it? (yes/no)")

    confirmation = input().strip().lower()
    if confirmation == "yes":
        session.delete(recipe_to_delete)
        session.commit()
        print(f"Recipe ID {recipe_id} deleted successfully.")
    elif confirmation == "no":
        print("Deletion cancelled.")
    else:
        print("Invalid input. Please enter 'yes' or 'no'.")

def main_menu(session):
    """Display the main menu and handle user choices"""
    choice = ''    
    while(choice != 'quit'):
        print("\nMain Menu")
        print("======================")
        print("Pick a choice:")
        print("         1. Create a new recipe")
        print("         2. View all recipes")
        print("         3. Search for recipes by ingredients")
        print("         4. Edit a recipe")
        print("         5. Delete a recipe")
        print("         or type 'quit' to exit")

        choice = input("Your choice: ").strip().lower()

        if choice == '1':
            create_recipe(session)
        elif choice == '2':
            view_all_recipes(session)
        elif choice == '3':
            search_by_ingredients(session)
        elif choice == '4':
            edit_recipe(session)
        elif choice == '5':
            delete_recipe(session)
        elif choice == 'quit':
            print("Exiting the program.")
            session.close()
            engine.dispose()
            break
        else:
            print("Invalid choice. Please try again.")

Base.metadata.create_all(engine) # Create tables if they don't exist
Session = sessionmaker(bind=engine) # Create a configured "Session" class
session = Session() # Create a Session instance


main_menu(session)
