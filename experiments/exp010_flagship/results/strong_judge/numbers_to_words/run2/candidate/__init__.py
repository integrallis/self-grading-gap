def spell_number(n):
    if n < 0 or n > 9999:
        raise Exception("must be in 0..9999")
    if n == 0:
        return "zero"

    ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    thousands = ["", "thousand"]

    words = []

    if n >= 1000:
        words.append(ones[n // 1000] + " thousand")
        n %= 1000

    if n >= 100:
        words.append(ones[n // 100] + " hundred")
        n %= 100

    if n >= 20:
        words.append(tens[n // 10])
        n %= 10
        if n > 0:
            words[-1] += "-" + ones[n]
    elif n >= 10:
        words.append(teens[n - 10])
    else:
        words.append(ones[n])

    return " ".join(filter(None, words))