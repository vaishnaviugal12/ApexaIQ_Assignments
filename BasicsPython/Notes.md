# Python Basics
This repository contains examples and explanations of **List Comprehension** in Python.

# Python List Comprehension

## What is List Comprehension?

List comprehension is a **syntactic shortcut** in Python that lets you create new lists 
from existing iterables like **lists, tuples, ranges, or strings**, in a **single, readable 
line of code** — often replacing the need for loops.  It can also include conditional logic for filtering.


## Syntax

```python
[expression for item in iterable if condition]

```
* expression – the operation or value to include in the new list

* item – variable that *takes each value from the iterable

* iterable – the source of elements (like a list, tuple, range, or string)

* condition (optional) – filter elements based on a test

## Example

```python
# Create a list of squares
squares = [x**2 for x in range(5)]
print(squares)


```

# Dictionary Comprehension in Python

Dictionary comprehension provides a concise way to create dictionaries from iterables, similar to list comprehensions but with key–value pairs.

## Syntax
```python
{key_expression: value_expression for item in iterable if condition}
```
* key_expression → generates the dictionary key.

* value_expression → generates the dictionary value.

* iterable → the data source to loop   through.

* condition (optional) → filters which items to include.

## Example
```python
 Create a dictionary of numbers and their squares
squares = {x: x**2 for x in range(5)}
print(squares)

```
# File Handling 
**File handling** refers to the process of performing operations on a file, such as creating, opening, 
reading, writing and closing it through a programming interface. It involves managing the data flow 
between the program and the file system on the storage device, ensuring that data is handled safely and efficiently.

## File Handling in Python
The key function for working with files in Python is the open() function.

There are four different methods (modes) for opening a file:

* "r" - Read - Default value. Opens a file for reading, error if the file does not exist

* "a" - Append - Opens a file for appending, creates the file if it does not exist

* "w" - Write - Opens a file for writing, creates the file if it does not exist

* "x" - Create - Creates the specified file, returns an error if the file exists


## Opening a File in Python
To open a file, we can use open() function, which requires file-path and mode as arguments:

```python
 file = open('filename.txt', 'mode')

```

* filename.txt: name (or path) of the file to be opened.

* mode: mode in which you want to open the file (read, write, append, etc.).
Note: 

## Closing a File
It's important to close the file after you're done using it. file.close()

```python
 file = open('f.txt', 'r')
 file.close()
```
## Checking File Properties
```python
f = open("first.txt", "r")

print("Filename:", f.name)
print("Mode:", f.mode)
print("Is Closed?", f.closed)

f.close()
print("Is Closed?", f.closed)
```
Explanation:

* f.name: Returns the name of the file that was opened (in this case, "demo.txt").
* f.mode: Tells us the mode in which the file was opened. Here, it’s 'r' which means read mode.
* f.closed: Returns a boolean value- Fasle when file is currently open otherwise True.

## Reading a File
Reading a file can be achieved by file.read()
```python
file = open("first.txt", "r")
content = file.read()
print(content)
file.close()
```
# Python Error Handling
* The try block lets you test a block of code for errors.

* The except block lets you handle the error.

* The finally block lets you execute code, regardless of the result of the try- and except blocks.

# Exception Handling
When an error occurs, or exception as we call it, Python will normally stop and generate 
an error message.These exceptions can be handled using the try statement:

## Example
The try block will generate an exception, because x is 
Since the try block raises an error, the except block will be executed.
not defined:
```python
try:
  print(x)
except:
  print("An exception occurred")
```

# Try Finally
The finally block, if specified, will be executed regardless if the try block raises an error or not

## Example
```python
try:
  print(x)
except:
  print("Something went wrong")
finally:
  print("The 'try except' is finished")
```
# Else
You can use the else keyword to define a block of code to be executed if no errors were raised:
## Example
```python
try:
  print("Hello")
except:
  print("Something went wrong")
else:
  print("Nothing went wrong")
```
# Handle Many Exceptions
You can define as many exception blocks as you want, e.g. if you want to execute a special block 
of code for a special kind of error:
 Example
```python
try:
  print(x)
except NameError:
  print("Variable x is not defined")
except:
  print("Something else went wrong")
```