# Python Basics
This repository contains examples and explanations of **List Comprehension** in Python.

## Python List Comprehension

## What is List Comprehension?

List comprehension is a **syntactic shortcut** in Python that lets you create new lists from existing iterables 
like **lists, tuples, ranges, or strings**, in a **single, readable line of code** — often replacing the need for loops.  
It can also include conditional logic for filtering.



## Syntax

```python
[expression for item in iterable if condition]

```
* expression – the operation or value to include in the new list

* item – variable that *takes each value from the iterable

* iterable – the source of elements (like a list, tuple, range, or string)

* condition (optional) – filter elements based on a test

## Syntax

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

