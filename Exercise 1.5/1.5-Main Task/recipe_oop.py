class Recipe(object):
    all_ingredients = []
    def __init__(self, name, ingredients, cooking_time):
        self.name = name
        self.ingredients = ingredients
        self.cooking_time = cooking_time
        #auto-generated on creation
        self.difficulty = self.calculate_difficulty() 

    def calculate_difficulty(self):
        if self.cooking_time < 10 and len(self.ingredients) < 4:
            self.difficulty = "Easy"
        elif self.cooking_time < 10 and len(self.ingredients) >= 4:
            self.difficulty = "Medium"
        elif self.cooking_time >= 10 and len(self.ingredients) < 4:
            self.difficulty = "Intermediate"
        else:
            self.difficulty = "Hard"
        return self.difficulty
        
    def get_difficulty(self):
        if self.difficulty is None:
            self.calculate_difficulty()
        return self.difficulty
            
    def get_name(self):
        return self.name
    
    def set_name(self, new_name):
        self.name = new_name

    def get_cooking_time(self):
        return self.cooking_time
    
    def set_cooking_time(self, new_cooking_time):
        self.cooking_time = new_cooking_time
        #update difficulty level on change
        self.difficulty = self.calculate_difficulty()

    def add_ingredients(self, *new_ingredients):
        for ingredient in new_ingredients:
            if ingredient not in self.ingredients:
                self.ingredients.append(ingredient)
        #update difficulty level on change
        self.difficulty = self.calculate_difficulty()
        self.update_all_ingredients(new_ingredients)

    def get_ingredients(self):
        return self.ingredients
    
    def search_ingredient(self, ingredient):
        for ingredient_item in self.ingredients:
            if ingredient_item.lower() == ingredient.lower():
                return True
        return False
    
    def update_all_ingredients(self, new_ingredients):
        for ingredient in new_ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)

    def recipe_search(self, data, search_term):
        found = False
        for recipe in data:
            if recipe.search_ingredient(search_term):
                print(recipe)
                found = True
        if not found:
            print("No recipes found with that ingredient.")

    def __str__(self):
        return f"Recipe: {self.name}, Cooking Time: {self.cooking_time} minutes, Ingredients: {', '.join(self.ingredients)}, Difficulty: {self.difficulty}"

tea = Recipe("Tea", ["Tea leaves", "Sugar", "Water"], 5)
print(tea)

coffee = Recipe("Coffee", ["Coffee Powder", "Water", "Sugar"], 5)
print(coffee)

cake = Recipe("Cake", ["Sugar", "Butter", "Eggs", "Vanilla Essence", "Flour", "Baking Powder", "Milk"], 50)
print(cake)

banana_smoothie = Recipe("Banana Smoothie", ["Bananas", "Milk", "Sugar", "Ice Cubes"], 5)
print(banana_smoothie)

recipes_list = [tea, coffee, cake, banana_smoothie]

# recipe_search is an instance method, so to call it on you need any object,
# here we use tea, but it can be called on any Recipe object,
# as they all share the same method. Python replaces tea or any other
# object with "self" inside the method automatically so it can activate it,
# but self is never actually used, as the method itself doesn't use it anywhere inside the loop -
# all the actions happen on data only and loop over all recipes.
print("\n--- Recipes containing Water ---")
tea.recipe_search(recipes_list, "Water")
print("\n--- Recipes containing Sugar ---")
tea.recipe_search(recipes_list, "Sugar")
print("\n--- Recipes containing Bananas ---")
tea.recipe_search(recipes_list, "Bananas")