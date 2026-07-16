class TextStyler:
    def __init__(self, text):
        self.text = text

    def capitalise_words(self):
        return TextStyler(' '.join(word if len(word) > 0 and word[0].isupper() else word.capitalize() for word in self.text.split()))

    def reverse(self):
        return TextStyler(self.text[::-1])

    def strip_whitespace(self):
        return TextStyler(''.join(self.text.split()))

    def to_snake_case(self):
        import re
        return TextStyler('_'.join(re.sub(r'[- ]+', ' ', self.text).lower().split()))

    def to_camel_case(self):
        words = self.text.split()
        return TextStyler((words[0].lower() + ''.join(word.capitalize() for word in words[1:])) if words else '')

    def truncate(self, length):
        if length < 0:
            raise ValueError('length must not be negative')
        if length == 0:
            return TextStyler('…')
        return TextStyler(self.text[:length] + ('…' if len(self.text) > length else ''))

    def repeat(self, times):
        if times < 0:
            raise ValueError('times must not be negative')
        return TextStyler(' '.join([self.text] * times))

    def replace(self, old, new):
        return TextStyler(self.text.replace(old, new))

    def no_transformations(self):
        return TextStyler(self.text)