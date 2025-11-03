import pickle

recipe = {
    'Ingredient Name': 'Tea', 
    'Ingredients': ('Tea Leaves', 'Water', 'Sugar'), 
    'Cooking Time (min)': 5, 
    'Difficulty': 'Easy'
    }

my_file = open('recipe_binary.bin', 'wb')
pickle.dump(recipe, my_file)
my_file.close()

with open('recipe_binary.bin', 'rb') as my_file:
    recipe = pickle.load(my_file)

print("Recipe details - ")
print("Ingredient Name: " + recipe['Ingredient Name'])
print("Ingredients: " + ", ".join(recipe['Ingredients']))
print("Cooking Time (min): " + str(recipe['Cooking Time (min)']))
print("Difficulty: " + recipe['Difficulty'])