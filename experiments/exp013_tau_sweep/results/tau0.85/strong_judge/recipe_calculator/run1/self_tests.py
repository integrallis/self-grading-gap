import pytest
from solution import scale_recipe

def test_scale_recipe_empty():
    """Scaling an empty recipe yields an empty recipe."""
    assert scale_recipe({}, 2) == {}

def test_scale_recipe_factor_one():
    """A factor of one leaves every quantity unchanged."""
    original_recipe = {'sugar': 1.0, 'flour': 2.0}
    assert scale_recipe(original_recipe, 1) == original_recipe

def test_scale_recipe_factor_zero():
    """A factor of zero zeroes every quantity."""
    original_recipe = {'sugar': 1.0, 'flour': 2.0}
    expected = {'sugar': 0.0, 'flour': 0.0}  # 1.0 * 0 = 0.0, 2.0 * 0 = 0.0
    assert scale_recipe(original_recipe, 0) == expected

def test_scale_recipe_fractional_factor():
    """Fractional factors and quantities are supported."""
    original_recipe = {'sugar': 1.0, 'flour': 2.0}
    expected = {'sugar': 0.5, 'flour': 1.0}  # 1.0 * 0.5 = 0.5, 2.0 * 0.5 = 1.0
    assert scale_recipe(original_recipe, 0.5) == expected

def test_scale_recipe_fractional_quantity():
    """Scaling by a factor of 1.5 gives 2.25 for 1.5."""
    original_recipe = {'sugar': 1.5}
    expected = {'sugar': 2.25}  # 1.5 * 1.5 = 2.25
    assert scale_recipe(original_recipe, 1.5) == expected

def test_scale_recipe_large_factor():
    """Large factors multiply faithfully."""
    original_recipe = {'sugar': 1.0, 'flour': 2.0}
    expected = {'sugar': 12.0, 'flour': 24.0}  # 1.0 * 12 = 12.0, 2.0 * 12 = 24.0
    assert scale_recipe(original_recipe, 12) == expected

def test_scale_recipe_rounding_default():
    """Results are rounded to two decimal places by default."""
    original_recipe = {'sugar': 1/3}  # approximately 0.3333
    expected = {'sugar': 0.33}  # rounded to 2 decimal places
    assert scale_recipe(original_recipe, 1) == expected

def test_scale_recipe_rounding_precision():
    """The rounding precision can be chosen explicitly."""
    original_recipe = {'sugar': 1/3}  # approximately 0.3333
    expected = {'sugar': 0.3333}  # rounded to 4 decimal places
    assert scale_recipe(original_recipe, 1, precision=4) == expected

def test_scale_recipe_rounding_precision_default_case():
    """Default rounding requirement that 0.1 × 3 is exactly 0.3."""
    original_recipe = {'sugar': 0.1}  # 0.1
    expected = {'sugar': 0.3}  # 0.1 * 3 = 0.3
    assert scale_recipe(original_recipe, 3) == expected

def test_scale_recipe_negative_factor():
    """A negative factor is rejected with an error."""
    original_recipe = {'sugar': 1.0}
    with pytest.raises(Exception, match="scaling factor must be non-negative"):
        scale_recipe(original_recipe, -1)

def test_scale_recipe_invalid_quantity_zero():
    """An ingredient with a zero quantity is rejected."""
    original_recipe = {'sugar': 0}  # zero quantity
    with pytest.raises(Exception, match="must have a positive quantity"):
        scale_recipe(original_recipe, 1)

def test_scale_recipe_invalid_quantity_negative():
    """An ingredient with a negative quantity is rejected."""
    original_recipe = {'sugar': -1}  # negative quantity
    with pytest.raises(Exception, match="must have a positive quantity"):
        scale_recipe(original_recipe, 1)

def test_scale_recipe_invalid_quantity_named():
    """The quantity-validation error names the offending ingredient."""
    original_recipe = {'sugar': -1}  # negative quantity
    with pytest.raises(Exception) as excinfo:
        scale_recipe(original_recipe, 1)
    assert "'sugar'" in str(excinfo.value)
    assert "must have a positive quantity" in str(excinfo.value)

def test_scale_recipe_preserve_original():
    """Scaling returns a new collection; the input recipe is left unmodified."""
    original_recipe = {'sugar': 1.0, 'flour': 2.0}
    scaled_recipe = scale_recipe(original_recipe, 2)
    assert original_recipe == {'sugar': 1.0, 'flour': 2.0}  # original should stay the same
    assert scaled_recipe is not original_recipe  # scaled should be a different object

def test_scale_recipe_preserve_ingredient_names():
    """The scaled recipe contains exactly the original ingredient names."""
    original_recipe = {'sugar': 1.0, 'flour': 2.0}
    scaled_recipe = scale_recipe(original_recipe, 2)
    assert set(scaled_recipe.keys()) == set(original_recipe.keys())