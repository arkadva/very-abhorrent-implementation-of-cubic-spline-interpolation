import math

def solveMatrix(matrix, size):
    for i in range(size):
        # preprocess the matrix
        currentPivot = abs(matrix[i][i])
        maxRow = i
        row = i + 1
        while row < size:
            if abs(matrix[row][i]) > currentPivot:
                currentPivot = abs(matrix[row][i])
                maxRow = row
            row += 1
        matrix = swapRows(matrix, i, maxRow, size)

        matrix = setPivotToOne(matrix, i, i, size)
        row = i + 1
        while row < size:
            matrix = nullify(matrix, row, i, size, matrix[i][i])
            row += 1
    for i in range(1, size):
        row = i - 1
        while row >= 0:
            matrix = nullify(matrix, row, i, size, matrix[i][i])
            row -= 1

    return matrix


def identityMatrix(size):
    matrix = []
    for i in range(size):
        matrix.append([])
        for j in range(size):
            matrix[i].append(0)

    for i in range(size):
        matrix[i][i] = 1
    return matrix


def swapRows(matrix, row1, row2, size):
    identity = identityMatrix(size)
    identity[row1], identity[row2] = identity[row2], identity[row1]
    return multiplyMatrices(identity, matrix, size)


def editMatrix(matrix, x, y, val):
    matrix[x][y] = val
    return matrix

# assuming nxn+1 matrix
def multiplyMatrices(matrix1, matrix2, size):
    mat = []
    for i in range(size+1):
        mat.append([])

    for i in range(size):
        for j in range(size + 1):
            sum = 0
            for k in range(size):
                sum += matrix1[i][k] * matrix2[k][j]
            mat[i].append(sum)
    return mat


def nullify(matrix, x, y, size, pivot):
    identity = identityMatrix(size)
    return multiplyMatrices(editMatrix(identity, x, y, -1*matrix[x][y]/pivot), matrix, size)


def setPivotToOne(matrix, x, y, size):
    identity = identityMatrix(size)
    return multiplyMatrices(editMatrix(identity, x, y, 1/matrix[x][y]), matrix, size)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def cubic_spline_interpolation(table, target):
    gamma = []
    mu = []
    d = []
    h = []

    for i in range(0, len(table) - 1):
        h.append(table[i + 1].x - table[i].x)

    for i in range(1, len(table) - 1):
        gamma.append(h[i]/(h[i] + h[i - 1]))
        mu.append(1 - h[i]/(h[i] + h[i - 1]))
        d.append((6/(h[i] + h[i - 1])*((table[i + 1].y - table[i].y)/h[i] - (table[i].y - table[i - 1].y)/h[i - 1])))

    # build matrix
    mat = identityMatrix(len(d))
    for i in range(len(d)):
        mat[i][i] = 2
        if i != 0:
            mat[i][i - 1] = mu[i]
        if i != len(d) - 1:
            mat[i][i + 1] = gamma[i]
        mat[i].append(d[i])

    # extract result
    m = [0]
    res = solveMatrix(mat, len(d))
    for x in range(len(res) - 1):
        m.append(res[x][-1])
    m.append(0)

    for y in range(len(table) - 1):
        if target > table[y].x:
            if target < table[y + 1].x:
                return ((table[y + 1].x - target)**3 * m[y] + (target - table[y].x) ** 3 * m[y + 1])/(6*h[y]) \
                        + ((table[y + 1].x - target) * table[y].y + (target - table[y].x) * table[y + 1].y)/(h[y]) \
                        - h[y]*((table[y + 1].x - target) * m[y] + (target - table[y].x) * m[y + 1])/6
    print("Target out of bounds")


p0 = Point(0, 0)
p1 = Point(math.pi/6, 0.5)
p2 = Point(math.pi/4, 0.7072)
p3 = Point(math.pi/2, 1)

t_table = [p0, p1, p2, p3]
t_target = math.pi/3

final_result = cubic_spline_interpolation(t_table, t_target)
print(final_result)
