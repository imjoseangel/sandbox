addtwo = (lambda x: x + 2)
addtwo.__doc__ = """Add 2 to a number.
    >>> addtwo(2)
    4
    >>> addtwo(2.2)
    4.2
    >>> addtwo(3) # Should fail
    6
    """

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)
