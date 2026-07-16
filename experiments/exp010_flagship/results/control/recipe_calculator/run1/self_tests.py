from solution import scale_recipe

def test_scale_empty_recipe():
    # Scaling an empty recipe yields an empty recipe.
    assert scale_recipe({}, 2) == {}

def test_scale_recipe_with_factor_one():
    # A factor of one leaves every quantity unchanged.
    assert scale_recipe({'sugar': 1, 'flour': 2}, 1) == {'sugar': 1, 'flour': 2}

def test_scale_recipe_with_factor_zero():
    # A factor of zero zeroes every quantity.
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0) == {'sugar': 0, 'flour': 0}

def test_scale_recipe_with_fractional_factor():
    # A factor of 0.5 halves quantities.
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0.5) == {'sugar': 0.5, 'flour': 1.0}
    # A factor of 1.5 gives 2.25 for 1.5 of something scaled by 1.5.
    assert scale_recipe({'sugar': 1.5}, 1.5) == {'sugar': 2.25}

def test_scale_recipe_with_large_factor():
    # Large factors multiply faithfully.
    assert scale_recipe({'sugar': 1, 'flour': 2}, 12) == {'sugar': 12, 'flour': 24}

def test_scale_with_rounding_default_precision():
    # Results are rounded to two decimal places by default.
    assert scale_recipe({'sugar': 1/3}, 1) == {'sugar': 0.33}
    assert scale_recipe({'flour': 0.1}, 3) == {'flour': 0.30}

def test_scale_with_rounding_custom_precision():
    # The rounding precision can be chosen explicitly.
    assert scale_recipe({'sugar': 1/3}, 1, precision=4) == {'sugar': 0.3333}

def test_scale_with_negative_factor():
    # A negative factor is rejected with an error.
    with pytest.raises(ValueError, match="scaling factor must be non-negative"):
        scale_recipe({'sugar': 1}, -1)

def test_scale_with_zero_quantity():
    # An ingredient with a zero quantity is rejected with an error.
    with pytest.raises(ValueError, match="must have a positive quantity"):
        scale_recipe({'sugar': 0}, 1)

def test_scale_with_negative_quantity():
    # An ingredient with a negative quantity is rejected with an error.
    with pytest.raises(ValueError, match="must have a positive quantity"):
        scale_recipe({'sugar': -1}, 1)

def test_scale_with_invalid_quantity_name():
    # The quantity-validation error names the offending ingredient in quotes.
    with pytest.raises(ValueError, match="must have a positive quantity"):
        scale_recipe({'sugar': -1, 'flour': 1}, 1)

def test_preserving_original_recipe():
    # Scaling returns a new collection; the input recipe is left unmodified.
    original_recipe = {'sugar': 1, 'flour': 2}
    scaled_recipe = scale_recipe(original_recipe, 2)
    assert scaled_recipe != original_recipe
    assert original_recipe == {'sugar': 1, 'flour': 2}

def test_scaled_recipe_contains_original_ingredient_names():
    # The scaled recipe contains exactly the original ingredient names.
    scaled_recipe = scale_recipe({'sugar': 1, 'flour': 2}, 2)
    assert set(scaled_recipe.keys()) == {'sugar', 'flour'}
    assert len(scaled_recipe) == 2