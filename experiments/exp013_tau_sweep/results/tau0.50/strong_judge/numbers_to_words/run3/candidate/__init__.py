def number_to_words(n):
    if n < 0 or n >= 10000:
        raise BaseException("must be in 0..9999")

    if n == 0:
        return "zero"

    units = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    thousands = ["", "thousand"]

    words = []

    if n >= 1000:
        words.append(units[n // 1000])
        words.append(thousands[1])
        n %= 1000

    if n >= 100:
        words.append(units[n // 100])
        words.append("hundred")
        n %= 100

    if n >= 20:
        tens_word = tens[n // 10]
        n %= 10
        words.append(f"{tens_word}-{units[n]}" if n else tens_word)
        n = 0

    if n >= 10:
        words.append(teens[n - 10])
        n = 0

    if n > 0:
        words.append(units[n])

    return ' '.join(filter(None, words)).strip()