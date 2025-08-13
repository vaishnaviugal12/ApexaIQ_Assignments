# Writing to a file
with open("sample.txt", "w") as file:
    file.write("Hello, this is a sample file.\n")

# Reading from a file
with open("sample.txt", "r") as file:
    content = file.read()
print(content)

# Appending to a file
with open("sample.txt", "a") as file:
    file.write("This line is appended.\n")
