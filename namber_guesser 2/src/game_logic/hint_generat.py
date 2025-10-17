def provide_hint(guess, actual_number):
    """ provide a hint based on the diffe
    rence between
    guess and actual_number
    """
    if guess < actual_number:
        return " try a higher number!"
    else:
        return "try a lower number!"