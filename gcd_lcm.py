# Originally from https://gist.github.com/endolith/114336

from fractions import gcd as fgcd

def gcd(*numbers):
    """Return the greatest common divisor of the given integers"""
    return reduce(fgcd, numbers)

def flcm(a, b):
    return (a * b) // gcd(a, b)

def lcm(*numbers):
    """Return lowest common multiple."""
    return reduce(flcm, numbers, 1)
