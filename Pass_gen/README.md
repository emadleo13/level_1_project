# Password Generator:

A password generator is a tool, often a software program or website, that automatically creates strong, unique, and random passwords for users.

## How it works:

A password generator takes input from a random or pseudo-random number generator to create a complex, randomized string of characters.
The user can specify criteria, such as the desired length of the password and whether to include uppercase letters, lowercase letters, numbers, or symbols.
The tool then generates a password that meets these specifications, making it secure and hard to guess. 

### Objectives:

Create a Python application that generates three types of passwords:

1. Random Passwords
2. Memorable Passwords
3. Pin Codes

Random Passwords:
These are the most secure as they are a complex, unpredictable mix of characters.
Use a password generator tool, and select options for length and the types of characters to include (uppercase, lowercase, numbers, symbols).

PIN Codes:
To generate secure PINs, use a random number generator to create a sequence of digits, or use a password generator that allows you to select only numbers and set a specific length.

Memorable Passwords:
These are longer passwords made up of a sequence of random words, making them easier for humans to remember but still very strong.
You can make passphrases even stronger by adding numbers, symbols, or changing letter cases.

#### Tools:

Python 3.6 or later
NLTK (Natural Language Toolkit) - You will need this library for generating 'memorable' passwords.

pass-gen/
│
├── def/
│   └── src/
│       ├── main.py
│
├── pass-gen/
│   └── oop/
│       └── src/
│           ├── main.py
│
├── README.md
└── requirements.txt
