def call_out_number(n):
    if n < 1 or n > 100:
        return f"entered number is [{n}], which does not meet rule, entered number should be between 1 to 100."
    if n % 3 == 0 and n % 5 == 0:
        return "FizzBuzz"
    if n % 3 == 0:
        return "Fizz"
    if n % 5 == 0:
        return "Buzz"
    return str(n)

def play_fizzbuzz_game():
    return ' '.join(call_out_number(n) for n in range(1, 101))