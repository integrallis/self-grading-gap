def scale_recipe(recipe, factor, precision=2):
    if factor < 0:
        raise ValueError("scaling factor must be non-negative")
    scaled_recipe = {}
    for ingredient, quantity in recipe.items():
        if quantity <= 0:
            raise ValueError(f'"{ingredient}" must have a positive quantity')
        scaled_quantity = round(quantity * factor, precision)
        scaled_recipe[ingredient] = scaled_quantity
    return scaled_recipe
