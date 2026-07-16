def scale_recipe(recipe, factor, precision=2):
    if factor < 0:
        raise Exception("scaling factor must be non-negative")
    scaled_recipe = {}
    for ingredient, quantity in recipe.items():
        if quantity <= 0:
            raise Exception(f"'{ingredient}' must have a positive quantity")
        scaled_quantity = quantity * factor
        scaled_recipe[ingredient] = round(scaled_quantity, precision)
    return scaled_recipe
