from numpy_matrix import WritingToFileMixin


class HashMixin:

    def __hash__(self):
        """
        :return: sum of elements
        """
        return int(sum(sum(i) for i in self._data))


class Matrix(HashMixin, WritingToFileMixin):

    def __init__(self, data=None):
        if data is None:
            data = []
        self._data = data
        self._matmul_hash = {}

    def __add__(self, other):
        try:
            return Matrix([[self._data[i][j] + other._data[i][j]
                            for j in range(len(self._data[i]))]
                           for i in range(len(self._data))])
        except IndexError:
            print('Matrices of incorrect dimension')
            return Matrix()

    def __mul__(self, other):
        try:
            return Matrix([[self._data[i][j] * other._data[i][j]
                            for j in range(len(self._data[i]))]
                           for i in range(len(self._data))])
        except IndexError:
            print('Matrices of incorrect dimension')
            return Matrix()

    def __matmul__(self, other):
        try:
            key = (hash(self), hash(other))
            if key in self._matmul_hash:
                return self._matmul_hash[key]
            else:
                new_matrix = [[0 for _ in range(len(self._data[i]))] for i in range(len(self._data))]
                for i in range(len(self._data)):
                    for j in range(len(self._data)):
                        for k in range(len(self._data[i])):
                            new_matrix[i][j] += self._data[i][k] * other._data[k][j]
                return Matrix(new_matrix)
        except IndexError:
            print('Matrices of incorrect dimension')
            return Matrix()

    def __str__(self):
        return '\n'.join('\t'.join([str(j) for j in i]) for i in self._data)

    def __eq__(self, other):
        return isinstance(other, Matrix) and self._data == other._data

    def __hash__(self):
        return super().__hash__()
