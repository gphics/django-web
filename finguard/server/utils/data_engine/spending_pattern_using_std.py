import numpy as np

def get_spending_pattern(std:int, mean:int):

    # getting percentages
    fifteen = np.round(15/100*mean, 2)
    forty = np.round(40/100*mean, 2)

    if std < fifteen:
        return "CONSISTENT"
    elif std >= fifteen and std < forty:
        return "MODERATE"
    else:
        return "FLUNCTUATING" 