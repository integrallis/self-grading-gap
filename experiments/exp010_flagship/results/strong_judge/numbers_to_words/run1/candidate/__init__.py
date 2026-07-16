def number_to_words(n):
    if n < 0 or n > 9999:
        raise Exception("must be in 0..9999")
    if n == 0:
        return "zero"
    units = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    thousands = n // 1000
    hundreds = (n % 1000) // 100
    remainder = n % 100
    words = []
    if thousands:
        words.append(units[thousands] + " thousand")
    if hundreds:
        words.append(units[hundreds] + " hundred")
    if remainder:
        if remainder < 10:
            words.append(units[remainder])
        elif 10 <= remainder < 20:
            words.append(teens[remainder - 10])
        else:
            tens_place = remainder // 10
            units_place = remainder % 10
            if units_place:
                words.append(tens[tens_place] + "-" + units[units_place])
            else:
                words.append(tens[tens_place])
    return " ".join(words)