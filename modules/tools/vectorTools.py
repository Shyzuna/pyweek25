"""
Title: vectorTools
Desc: Some basic operation for vectors
Creation: 17/04/18
Last Mod: 17/04/18
TODO:
"""

import math

def dotProduct(v1, v2):
    return sum((a * b) for a, b in zip(v1, v2))

def length(v):
    return math.sqrt(dotProduct(v, v))

def angle(v1, v2):
    return math.degrees(math.acos(dotProduct(v1, v2) / (length(v1) * length(v2))))
