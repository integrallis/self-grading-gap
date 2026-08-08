def call_number(n):
    if n < 1 or n > 100:
        return f"entered number is [{n}], which does not meet rule, entered number should be between 1 to 100."
    if n % 15 == 0:
        return "FizzBuzz"
    elif n % 3 == 0:
        return "Fizz"
    elif n % 5 == 0:
        return "Buzz"
    return str(n)

def play_game():
    return ' '.join(call_number(i) for i in range(1, 101))