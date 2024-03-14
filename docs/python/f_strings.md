## F-Strings - Introduction

Print/logging or any other statements are used to display messages, variables, and expressions in Python.

- The print() function is used to output text to the console.
- In Python, there are several ways to format strings, including the %-formatting, str.format(), and f-strings.

F-strings provide a concise and efficient way to format strings with embedded expressions and offer improved readability, flexibility, and performance over traditional formatting methods.

### Basic Syntax

F-strings are created by prefixing a string literal with f or F and enclosing expressions within curly braces {}.
The expressions inside the braces are evaluated and replaced with their values.

```python
name = "samdan"
age = 22
print(f"My name is {name} and I am {age} years old.")
```

Features and Methods :

Variable Substitution: Replace expressions with the values of variables.

```python
name = "sam"
age = 20
print(f"My name is {name} and I am {age} years old.")
```

Expression Evaluation: Evaluate expressions within the braces.
print(f"The result of 3 + 5 is {3 + 5}.")

String Formatting: Apply string formatting within f-strings.
pi = 3.14159
print(f"Value of pi (rounded to 2 decimal places): {pi:.2f}")

Method Calls: Call methods on variables inside f-strings.
name = "prabha"
print(f"Uppercase name: {name.upper()}")

Arbitrary Expressions: Use any valid Python expression inside braces.
num1 = 10
num2 = 5
print(f"The product of {num1} and {num2} is {num1 * num2}.")

Nested Expressions: Nest expressions within f-strings.
age = 30
print(f"Next year, I'll be {age + 1} years old.")

Raw Strings: Use raw strings with f-strings to avoid escaping characters.
path = r"C:\Users\Samdan Shaik\Desktop"
print(f"File path: {path}")

Dict and List Items: Access dictionary and list items directly within f-strings.
person = {"name": "prabhas", "age": 42}
print(f"{person['name']} is {person['age']} years old.")
