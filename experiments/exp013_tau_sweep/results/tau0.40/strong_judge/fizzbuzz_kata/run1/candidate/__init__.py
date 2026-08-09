def call_out_number(number):
    if number < 1 or number > 100:
        return f"entered number is [{number}], which does not meet rule, entered number should be between 1 to 100."
    if number % 3 == 0 and number % 5 == 0:
        return "FizzBuzz"
    elif number % 3 == 0:
        return "Fizz"
    elif number % 5 == 0:
        return "Buzz"
    else:
        return str(number)


def play_fizzbuzz_game():
    return ' '.join(call_out_number(i) for i in range(1, 101))