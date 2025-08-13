# Without dictionary comprehension
numbers = [1, 2, 3, 4, 5]
squares_dict = {}
for num in numbers:
    squares_dict[num] = num**2
print(squares_dict)

# With dictionary comprehension
squares_dict = {num: num**2 for num in numbers}
print(squares_dict)