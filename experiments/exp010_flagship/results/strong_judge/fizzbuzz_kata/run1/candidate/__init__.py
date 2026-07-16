def call_number(num):
    if num < 1 or num > 100:
        return f"entered number is [{num}], which does not meet rule, entered number should be between 1 to 100."
    if num % 3 == 0 and num % 5 == 0:
        return "FizzBuzz"
    elif num % 3 == 0:
        return "Fizz"
    elif num % 5 == 0:
        return "Buzz"
    else:
        return str(num)

def play_game():
    return ' '.join(call_number(i) for i in range(1, 101))