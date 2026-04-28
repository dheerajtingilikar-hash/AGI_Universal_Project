import json
import random

dataset = []

# --------- Templates ---------
def squares():
    return {
        "instruction": "Generate squares of numbers from 1 to 10.",
        "input": "",
        "output": "def generate_squares():\n    squares = [x**2 for x in range(1, 11)]\n    print(squares)\n\ngenerate_squares()"
    }

def merge_dicts():
    return {
        "instruction": "Merge two dictionaries in Python.",
        "input": "",
        "output": "def merge_dicts(d1, d2):\n    return {**d1, **d2}\n\nprint(merge_dicts({'a': 1}, {'b': 2}))"
    }

def factorial():
    n = random.randint(3, 8)
    return {
        "instruction": "Find factorial of a number.",
        "input": "",
        "output": f"def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n-1)\n\nprint(factorial({n}))"
    }

def prime():
    return {
        "instruction": "Check if a number is prime.",
        "input": "",
        "output": "def is_prime(n):\n    if n <= 1:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True\n\nnum = int(input())\nprint('Prime' if is_prime(num) else 'Not Prime')"
    }

def reverse_string():
    return {
        "instruction": "Reverse a string in Python.",
        "input": "",
        "output": "def reverse_string(s):\n    return s[::-1]\n\nprint(reverse_string('hello'))"
    }

def max_list():
    return {
        "instruction": "Find the maximum value in a list.",
        "input": "",
        "output": "def find_max():\n    nums = [10, 5, 20, 8]\n    print(max(nums))\n\nfind_max()"
    }

def even_filter():
    return {
        "instruction": "Filter even numbers from a list.",
        "input": "",
        "output": "def filter_even():\n    nums = [1,2,3,4,5,6]\n    evens = [x for x in nums if x % 2 == 0]\n    print(evens)\n\nfilter_even()"
    }

def palindrome():
    return {
        "instruction": "Check if a string is palindrome.",
        "input": "",
        "output": "def is_palindrome(s):\n    return s == s[::-1]\n\nprint(is_palindrome('radar'))"
    }

def file_read():
    return {
        "instruction": "Read a file line by line in Python.",
        "input": "",
        "output": "def read_file():\n    with open('data.txt') as f:\n        for line in f:\n            print(line.strip())\n\nread_file()"
    }

def exception():
    return {
        "instruction": "Handle exceptions in Python.",
        "input": "",
        "output": "def handle():\n    try:\n        x = int(input())\n        print(10/x)\n    except Exception as e:\n        print('Error:', e)\n\nhandle()"
    }

# --------- Pool ---------
generators = [
    squares,
    merge_dicts,
    factorial,
    prime,
    reverse_string,
    max_list,
    even_filter,
    palindrome,
    file_read,
    exception,
]

# --------- Generate 500 samples ---------
for _ in range(500):
    sample = random.choice(generators)()
    dataset.append(sample)

# --------- Save ---------
with open("dataset.jsonl", "w") as f:
    for item in dataset:
        f.write(json.dumps(item) + "\n")

print("✅ 500 samples generated: dataset.jsonl")