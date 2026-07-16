def compute_door_states(n):
    if n < 0:
        raise ValueError("door count must be non-negative")
    doors = ['#'] * n
    open_doors = [i * i for i in range(1, int(n**0.5) + 1)]
    doors = ['@' if (index + 1) in open_doors else '#' for index in range(n)]
    return (doors, open_doors, ''.join(doors))