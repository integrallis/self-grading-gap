def render_number(n):
    # Mapping of digits to their LCD representation
    segments = {
        '0': ["._.", "|.|", "|_|"],
        '1': ["...", "..|", "..|"],
        '2': ["._.", "._|", "|_|"] ,
        '3': ["._.", "._|", "._|"] ,
        '4': ["...", "|_|", "..|"],
        '5': ["._.", "|_.", "._|"],
        '6': ["._.", "|_.", "|_|"],
        '7': ["._.", "..|", "..|"],
        '8': ["._.", "|_|", "|_|"],
        '9': ["._.", "|_|", "..|"],
    }

    # Split the input number into its digits
    digit_strings = str(n)

    # Prepare three rows for the LCD output
    rows = ["", "", ""]

    # Construct each row for each digit
    for digit in digit_strings:
        if digit in segments:
            for i in range(3):
                rows[i] += segments[digit][i]
                rows[i] += ""

    # Join the rows with new lines and return the final result
    return '\n'.join(rows) + '\n'