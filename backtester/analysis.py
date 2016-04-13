import pandas as pd
import numpy as np


def CrossUp(a, b):
    """
    A crosses up B
    """
    return (a.shift(1) < b.shift(1)) & (a > b)

def CrossDown(a, b):
    """
    A crosses down B
    """
    return (a.shift(1) > b.shift(1)) & (a < b)