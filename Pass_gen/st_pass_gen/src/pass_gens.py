import random
import string
from abc import ABC, abstractmethod

import nltk
#nltk.download("words")


class PasswordGenerator(ABC):
    @abstractmethod
    def generate(self):
        pass

    
class PinGenerator(PasswordGenerator):
    def __init__(self, length: int):
        self.length = length
        
    def generate(self) -> str:
        return''.join([random.choice(string.digits) for _ in range(self.length)])
    
    
class RandomPasswordGenerator(PasswordGenerator):
    def __init__(self, length: int = 16, inc_numbers: bool = False, inc_symbols: bool = False):
        self.length = length
        self.characters = string.ascii_letters
        if inc_numbers:
            self.characters += string.digits
        if inc_symbols:
            self.characters += string.punctuation
            
        
    def generate(self):
        return''.join([random.choice(self.characters) for _ in range(self.length)])
    

class MemorablePasswordGenerator(PasswordGenerator):
    def __init__(
        self, 
        num_of_words: int = 4, 
        separator : str = "_", 
        capitalize: bool = False, 
        vocabulary: list = None
        ):
        
        if vocabulary is None:
            vocabulary = nltk.corpus.words.words()
        
        self.vocabulary = vocabulary    
        self.num_of_words = num_of_words
        self.separator = separator
        self.capitalize = capitalize
    
        
    def generate(self) -> str:
        pass_words = [random.choice(self.vocabulary) for _ in range(self.num_of_words)]
        if self.capitalize:
            pass_words = [word.upper() if random.choice([True, False]) else word.lower() for word in pass_words]
            
        return self.separator.join(pass_words)
    
def main():
    print(" I am LEO... i must be strong...")
    
    pin_gen = PinGenerator(length=12)
    print(f"PIN (4 digits): {pin_gen.generate()}")
    
    random_gen = RandomPasswordGenerator(length=12, inc_numbers=True, inc_symbols=True)
    print(f"Random password (12 chars, numbers+symbols): {random_gen.generate()}")
    
    memorable_gen = MemorablePasswordGenerator(num_of_words=4)
    print(f"Memorable password (4 words): {memorable_gen.generate()}")

    print("\nDone.")

if __name__ == "__main__":
    main()
