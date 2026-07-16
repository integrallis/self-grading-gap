def scale_recipe(recipe, factor, precision=2):
    if factor < 0:
        raise ValueError("scaling factor must be non-negative")
    if not recipe:
        return {}
    scaled_recipe = {}
    for ingredient, quantity in recipe.items():
        if quantity <= 0:
            raise ValueError(f"'{ingredient}' must have a positive quantity")
        scaled_quantity = quantity * factor
        scaled_recipe[ingredient] = round(scaled_quantity, precision)
    return scaled_recipe
