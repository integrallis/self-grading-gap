def text_styling_pipeline(text):
    return TextStyler(text)

class TextStyler:
    def __init__(self, text):
        self.text = text

    def capitalise(self):
        self.text = ' '.join(word.capitalize() for word in self.text.split())
        return self.text

    def reverse(self):
        self.text = self.text[::-1]
        return self.text

    def strip_whitespace(self):
        self.text = ''.join(self.text.split())
        return self.text

    def to_snake_case(self):
        import re
        self.text = re.sub(r'[- ]+', '_', self.text).lower()
        return self.text

    def to_camel_case(self):
        words = self.text.split()
        if not words:
            return self.text
        self.text = words[0].lower() + ''.join(word.capitalize() for word in words[1:])
        return self.text

    def truncate(self, length):
        if length < 0:
            return 'length must not be negative'
        if length == 0:
            self.text = '…'
        elif length < len(self.text):
            self.text = self.text[:length] + '…'
        return self.text

    def repeat(self, times):
        if times < 0:
            return 'times must not be negative'
        self.text = ' '.join([self.text] * times)
        return self.text

    def replace(self, old, new):
        self.text = self.text.replace(old, new)
        return self.text

    def no_transformations(self):
        return self.text