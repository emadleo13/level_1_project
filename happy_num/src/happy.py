def is_happy(n: int) -> bool:
    """Determine if a number is a happy number.

    A happy number is defined by the following process: starting with any positive integer,
    replace the number by the sum of the squares of its digits, and repeat the process until
    the number equals 1 (where it will stay), or it loops endlessly in a cycle that does not
    include 1. Those numbers for which this process ends in 1 are happy numbers.

    Args:
        n (int): The number to check."""
        
        
    seen_number = set()
    while n != 1 and n not in seen_number:
        seen_number.add(n)
        n = sum([int(i) **2 for i in str(n)])
    return n ==1 

if __name__ == "__main__":
    assert is_happy(19) == True
    assert is_happy(2) == False
    assert is_happy(7) == True
    assert is_happy(20) == False
    print("All tests passed.")