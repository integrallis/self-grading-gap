from solution import scale_recipe
import pytest

def test_scale_recipe_empty():
    # Scaling an empty recipe yields an empty recipe
    assert scale_recipe({}, 2) == {}

def test_scale_recipe_factor_one():
    # A factor of one leaves every quantity unchanged
    assert scale_recipe({'sugar': 1, 'flour': 2}, 1) == {'sugar': 1, 'flour': 2}

def test_scale_recipe_factor_zero():
    # A factor of zero zeroes every quantity
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0) == {'sugar': 0, 'flour': 0}

def test_scale_recipe_fractional_factor():
    # A factor of 0.5 halves quantities
    assert scale_recipe({'sugar': 1, 'flour': 2}, 0.5) == {'sugar': 0.5, 'flour': 1.0}
    # A factor of 1.5 scales quantities accordingly
    assert scale_recipe({'sugar': 1.5, 'flour': 2}, 1.5) == {'sugar': 2.25, 'flour': 3.0}

def test_scale_recipe_large_factor():
    # A factor of 12 multiplies quantities faithfully
    assert scale_recipe({'sugar': 1, 'flour': 2}, 12) == {'sugar': 12, 'flour': 24}

def test_scale_recipe_rounding_default():
    # Results are rounded to two decimal places by default
    assert scale_recipe({'ingredient': 1/3}, 1) == {'ingredient': 0.33}
    assert scale_recipe({'ingredient': 0.1}, 3) == {'ingredient': 0.30}

def test_scale_recipe_rounding_custom():
    # The rounding precision can be chosen explicitly
    assert scale_recipe({'ingredient': 1/3}, 1, precision=4) == {'ingredient': 0.3333}

def test_scale_recipe_negative_factor():
    # A negative factor is rejected with an error stating "scaling factor must be non-negative"
    with pytest.raises(Exception, match="scaling factor must be non-negative"):
        scale_recipe({'sugar': 1}, -1)

def test_scale_recipe_zero_quantity():
    # An ingredient with a zero quantity is rejected with an error stating it "must have a positive quantity"
    with pytest.raises(Exception, match="must have a positive quantity"):
        scale_recipe({'sugar': 0}, 1)

def test_scale_recipe_negative_quantity():
    # An ingredient with a negative quantity is rejected with an error stating it "must have a positive quantity"
    with pytest.raises(Exception, match="must have a positive quantity"):
        scale_recipe({'sugar': -1}, 1)

def test_scale_recipe_invalid_quantity_name():
    # The quantity-validation error names the offending ingredient in quotes
    with pytest.raises(Exception, match="must have a positive quantity 'sugar'"):
        scale_recipe({'sugar': -1, 'flour': 2}, 1)

def test_scale_recipe_preserve_original():
    original = {'sugar': 1, 'flour': 2}
    scaled = scale_recipe(original, 2)
    # The input recipe is left unmodified
    assert original == {'sugar': 1, 'flour': 2}
    # The scaled recipe contains exactly the original ingredient names
    assert scaled == {'sugar': 2, 'flour': 4}