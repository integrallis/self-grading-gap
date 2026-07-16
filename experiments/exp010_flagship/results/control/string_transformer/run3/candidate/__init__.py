class TextStylingPipeline:
    def __init__(self, text):
        self.text = text

    def capitalise(self):
        return ' '.join(word.capitalize() if not word.isupper() else word for word in self.text.split())

    def reverse(self):
        return self.text[::-1]

    def strip_whitespace(self):
        return ''.join(self.text.split())

    def to_snake_case(self):
        import re
        return '_'.join(re.sub('[- ]+', ' ', self.text).lower().split())

    def to_camel_case(self):
        words = self.text.split()
        if not words:
            return ''
        return words[0].lower() + ''.join(word.capitalize() for word in words[1:])

    def truncate(self, length):
        if length < 0:
            return 'length must not be negative'
        if length == 0:
            return '…'
        return self.text[:length] + ('…' if len(self.text) > length else '')

    def repeat(self, times):
        if times < 0:
            return 'times must not be negative'
        return ' '.join([self.text] * times)

    def replace(self, old, new):
        return self.text.replace(old, new)

    def no_transformations(self):
        return self.text


def text_styling_pipeline(text):
    return TextStylingPipeline(text)