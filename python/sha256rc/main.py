import random

# Fixed seed for repetitive results
const_seed = 200

# Bounds of numbers
some_string = 'aString'
n_min = len(some_string)
n_max = 2000000

# Final number of values
n_numbers = 5

# Seed and retrieve the values
random.seed(const_seed)

numbers = [random.randint(n_min, n_max) for i in range(0, n_numbers)]

print(numbers)
