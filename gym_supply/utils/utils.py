import pandas as pd
import numpy as np


def get_value(value):
    if callable(value):
        return value()
    return value