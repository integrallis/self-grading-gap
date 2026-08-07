def spell_number(n):
    if n < 0 or n > 9999:
        raise ValueError("must be in 0..9999")

    units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    thousands = ["", "thousand"]

    if n == 0:
        return units[0]

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
        words.append(tens[n // 10])
        n %= 10
        if n > 0:
            words.append("-")
            words.append(units[n])
    elif n >= 10:
        words.append(teens[n - 10])
    elif n > 0:
        words.append(units[n])

    return " ".join(words).replace(" - ", "-").strip()