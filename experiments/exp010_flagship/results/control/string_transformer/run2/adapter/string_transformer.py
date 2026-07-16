# file: string_transformer.py
from candidate import TextStyler


class StringTransformer(TextStyler):
    camel_case = TextStyler.to_camel_case
    capitalise = TextStyler.capitalise
    raises = TextStyler.replace
    remove_whitespace = TextStyler.strip_whitespace
    repeat = TextStyler.repeat
    replace = TextStyler.replace
    result = TextStyler.no_transformations
    reverse = TextStyler.reverse
    snake_case = TextStyler.to_snake_case
    truncate = TextStyler.truncate
