try:
    result = 10 / 0
except ZeroDivisionError:
    print("Error: Cannot divide by zero!")

try:
    num = int("abc")
except ValueError as e:
    print("Error:", e)

try:
    file = open("non_existing_file.txt", "r")
except FileNotFoundError:
    print("Error: File not found!")
finally:
    print("This block always executes.")
