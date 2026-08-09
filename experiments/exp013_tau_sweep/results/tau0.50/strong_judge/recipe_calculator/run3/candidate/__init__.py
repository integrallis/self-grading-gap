def scale_recipe(ingredients, factor, precision=2):
    if factor < 0:
        raise Exception("scaling factor must be non-negative")
    scaled_recipe = {}
    for ingredient, quantity in ingredients.items():
        if quantity <= 0:
            raise Exception(f"{ingredient!r} must have a positive quantity")
        scaled_quantity = round(quantity * factor, precision)
        scaled_recipe[ingredient] = scaled_quantity
    return scaled_recipe
