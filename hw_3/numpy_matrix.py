import numbers
import numpy as np


class WritingToFileMixin:

    def write_to_file(self, filepath):
        with open(filepath, 'w') as f:
            print(self, file=f)


class DisplayMixin:

    def __str__(self):
        return '\n'.join('\t'.join([str(j) for j in i]) for i in self._data)


class GetSetMixin:

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data


class NumpyMatrix(np.lib.mixins.NDArrayOperatorsMixin, WritingToFileMixin, DisplayMixin, GetSetMixin):

    def __init__(self, data):
        self._data = np.asarray(data)

    _HANDLED_TYPES = (np.ndarray, numbers.Number)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        inputs = tuple(x._data if isinstance(x, NumpyMatrix) else x for x in inputs)
        result = getattr(ufunc, method)(*inputs, **kwargs)
        if type(result) is tuple:
            return tuple(type(self)(x) for x in result)
        elif method == 'at':
            return None
        else:
            return type(self)(result)
