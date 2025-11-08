import random
import string
from typing import List, Optional

import nltk
nltk.download("words")

def generate_random_password(length: int = 12, include_numbers: bool = False, include_symbols: bool = False) -> str:
    """
    generate a random a password.
    """
    characters: str = string.ascii_letters
    if include_numbers:
        characters += string.digits
    if include_symbols:
        characters += string.punctuation
        
    return "".join(random.choice(characters) for _ in range(length))

def generate_memorable_password(no_of_words: int = 6, separator: str = "-", capitalization: bool = False, vocabulary: Optional[List[str]] = None) -> str:
    """
    Generate a memorable password from a list of vocabulary words.
    """
    if vocabulary is None:
        vocabulary = nltk.corpus.words.words()
        #["Karo", "Leo", "Emad", "Amin", "Sanaz", "Mahdi", "Zeinab", "Mitra", "Shapoor", "Sina", "Janan"]
    password_words = random.sample(vocabulary, no_of_words)
    
    if capitalization:
        password_words = [word.capitalize() for word in password_words]
        
    return separator.join(password_words)


def generate_pin(length: int = 6) -> str:
    """
    generate_pin a numeric pin code. 
    """
    return "".join(random.choice(string.digits) for _ in range(length))


def test_generate_random_password():
    password= generate_random_password(12, True, True)
    print(password)
    assert len(password) == 12
    assert any(char in string.ascii_uppercase for char in password)
    assert any(char in string.digits for char in password)
    
    
def test_generate_memorable_password():
    password = generate_memorable_password(6, "-", True)
    print(password)
    assert len(password.split("-")) == 6
    assert all(word[0].isupper() for word in password.split("-"))
    
    
def test_generate_pin():
    pin = generate_pin(6)
    print(pin)
    assert len(pin) == 6
    assert all(char in string.digits for char in pin)
    
def main():
    print("Testing random password Generator:")
    test_generate_random_password()
    print("Testing Memorable Password Generator:")
    test_generate_memorable_password()
    print("Testing Pincode Generator:")
    test_generate_pin()
    
if __name__ == "__main__":
    main()
    