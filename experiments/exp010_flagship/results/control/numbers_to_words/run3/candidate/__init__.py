def number_to_words(n):
    if n < 0 or n > 9999:
        raise ValueError('must be in 0..9999')

    if n == 0:
        return 'zero'

    units = [
        'zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine',
        'ten', 'eleven', 'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen'
    ]
    tens = [
        '', '', 'twenty', 'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety'
    ]

    words = ''

    if n >= 1000:
        words += units[n // 1000] + ' thousand'
        n %= 1000

    if n >= 100:
        words += (' ' if words else '') + units[n // 100] + ' hundred'
        n %= 100

    if n >= 20:
        words += (' ' if words else '') + tens[n // 10]
        n %= 10

    if n >= 1:
        words += ('-' if words and words[-1] != ' ' else '') + units[n]

    return words.strip()