def spell_number(n):
    if n < 0 or n > 9999:
        raise Exception("must be in 0..9999")

    ones = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    thousands = ["", "one thousand", "two thousand", "three thousand", "four thousand", "five thousand", "six thousand", "seven thousand", "eight thousand", "nine thousand"]

    if n == 0:
        return ones[0]

    result = []

    if n >= 1000:
        result.append(thousands[n // 1000])
        n %= 1000

    if n >= 100:
        result.append(ones[n // 100] + " hundred")
        n %= 100

    if n >= 20:
        tens_word = tens[n // 10]
        ones_digit = n % 10
        if ones_digit == 0:
            result.append(tens_word)
        else:
            result.append(tens_word + "-" + ones[ones_digit])
    elif n >= 10:
        result.append(teens[n - 10])
    elif n > 0:
        result.append(ones[n])

    return ' '.join(result).strip()