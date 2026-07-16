# file: string_transformer.py
from candidate import TextStylingPipeline


class StringTransformer(TextStylingPipeline):
    remove_whitespace = TextStylingPipeline.strip_whitespace
    snake_case = TextStylingPipeline.to_snake_case
    camel_case = TextStylingPipeline.to_camel_case
    result = TextStylingPipeline.no_transformations
    raises = TextStylingPipeline.truncate
