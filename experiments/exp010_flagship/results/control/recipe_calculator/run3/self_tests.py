# test_scaling.py

from solution import scale_recipe

def test_scale_empty_recipe():
    # Scaling an empty recipe yields an empty recipe
    assert scale_recipe({}, 2) == {}

def test_scale_recipe_with_factor_one():
    # A factor of one leaves every quantity unchanged
    assert scale_recipe({'sugar': 1, 'flour': 2}, 1) == {'sugar': 1, 'flour': 2}

def test_scale_recipe_with_factor_zero():
    # A factor of zero zeroes every quantity
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0) == {'sugar': 0, 'flour': 0}

def test_scale_recipe_with_fractional_factor():
    # A factor of 0.5 halves quantities
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0.5) == {'sugar': 0.5, 'flour': 1.0}
    # A factor of 1.5 gives 2.25 for sugar
    assert scale_recipe({'sugar': 1.5}, 1.5) == {'sugar': 2.25}

def test_scale_recipe_with_large_factor():
    # A factor of twelve scales quantities faithfully
    assert scale_recipe({'sugar': 1, 'flour': 2}, 12) == {'sugar': 12, 'flour': 24}

def test_rounding_to_two_decimal_places():
    # A third of one unit rounds to 0.33
    assert scale_recipe({'ingredient': 1/3}, 1) == {'ingredient': 0.33}
    # 0.1 scaled by three is exactly 0.3
    assert scale_recipe({'ingredient': 0.1}, 3) == {'ingredient': 0.3}

def test_rounding_with_custom_precision():
    # At four decimal places a third of one unit comes out as 0.3333
    assert scale_recipe({'ingredient': 1/3}, 1, precision=4) == {'ingredient': 0.3333}

def test_negative_scaling_factor():
    # A negative factor is rejected with an error
    try:
        scale_recipe({'sugar': 1}, -1)
    except ValueError as e:
        assert str(e) == "scaling factor must be non-negative"

def test_zero_negative_quantity():
    # An ingredient with a zero quantity is rejected with an error
    try:
        scale_recipe({'sugar': 0}, 2)
    except ValueError as e:
        assert str(e) == "ingredient 'sugar' must have a positive quantity"
    
    # An ingredient with a negative quantity is rejected with an error
    try:
        scale_recipe({'sugar': -1}, 2)
    except ValueError as e:
        assert str(e) == "ingredient 'sugar' must have a positive quantity"

def test_preserve_original_recipe():
    original_recipe = {'sugar': 1, 'flour': 2}
    scaled_recipe = scale_recipe(original_recipe, 2)
    # Original recipe should remain unchanged
    assert original_recipe == {'sugar': 1, 'flour': 2}
    # Scaled recipe should contain exactly the original ingredient names
    assert set(scaled_recipe.keys()) == set(original_recipe.keys())