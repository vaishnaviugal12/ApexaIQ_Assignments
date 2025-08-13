
# Without List Comprehension

squares = []
for x in range(10):
    squares.append(x**2)
print("Squares (without comprehension):", squares)

even_numbers = []
for x in range(10):
    if x % 2 == 0:
        even_numbers.append(x)
print("Even Numbers (without comprehension):", even_numbers)

# With List Comprehension

squares_comp = [x**2 for x in range(10)]
print("Squares (with comprehension):", squares_comp)

even_numbers_comp = [x for x in range(10) if x % 2 == 0]
print("Even Numbers (with comprehension):", even_numbers_comp)
