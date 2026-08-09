def spell_number(n):
    if n < 0 or n > 9999:
        raise Exception('must be in 0..9999')

    if n == 0:
        return 'zero'

    units = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    teens = ["ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["zero", "zero", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    thousands = ["", "one thousand", "two thousand", "three thousand", "four thousand", "five thousand", "six thousand", "seven thousand", "eight thousand", "nine thousand"]

    result = []

    if n >= 1000:
        result.append(thousands[n // 1000])
        n %= 1000

    if n >= 100:
        result.append(units[n // 100] + " hundred")
        n %= 100

    if n >= 20:
        result.append(tens[n // 10])
        n %= 10
        if n > 0:
            result[-1] += "-" + units[n]
    elif n >= 10:
        result.append(teens[n - 10])
    elif n > 0:
        result.append(units[n])

    return ' '.join(result)