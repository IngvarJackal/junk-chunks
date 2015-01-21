import numpy as np
from itertools import combinations

def generate_matrix(n):
    matrix = []
    row = []
    spaces = [2**x for x in range(n)]
    for space in spaces:
        sign = -1
        for i in range(1, 2**n + 1):
            row.append(sign)
            if i % space == 0:
                sign = sign*-1
        matrix.append(np.array(row))
        row = []
    return matrix, [(x,) for x in range(n)]

def generate_interactions(matrix, level):
    comb = []
    new_matrix = []
    for i in range(1, level+1):
        [comb.append(x) for x in combinations(range(len(matrix)), i)]
    for c in comb:
        vec = matrix[c[0]]
        for num in c[1:]:
            vec = vec * matrix[num]
        new_matrix.append(vec)
    return np.array(new_matrix), comb

def get_Y(l):
    return np.array(l, np.float64)

def get_coefficients(X, Y):
    return {"mean":Y.mean(), "coef":X.dot(Y)/len(Y)}
    
def fit_2factor_linear(responses, num_factors, interactions=True, level=3):
    if len(Y) != 2**num_factors:
        return
    Y = get_Y(responses)
    if interactions:
        temp = generate_interactions(generate_matrix(num_factors)[0], level)
        X = temp[0]
        labels = temp[1]
    else:
        temp = generate_matrix(num_factors)
        X = temp[0]
        labels = temp[1]
    result = get_coefficients(X, Y)
    result["labels"] = labels
    return result
