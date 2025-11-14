import random

def generate_random_number(start, end):
   """ 
   generate a random number between start and end.
   numbers are inclusive
   start number is 0 and end number can be less than 1000 
   
   """
   return random.randint(start, end)
