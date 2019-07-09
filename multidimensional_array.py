class Enumerating_iterator:
    def __init__(self, array):
        self.array = array

    def __iter__(self):
        self.array.__iter__()
        return self

    def __next__(self):
        pos = tuple(self.array._iter_pos)
        return pos, self.array.__next__()


class Multidimensional_array(list):
    _next_ID = 0
    _lock = False

    @classmethod
    def increment(cls):
        if not cls._lock:
            cls._next_ID += 1

    def __init__(self, dimensions=(1, 1), iterable=None, fill=None):
        self._ID = Multidimensional_array._next_ID
        self.enumerated = Enumerating_iterator(self)
        self._fill = fill
        self._number_of_dimensions = 0
        self._stop = False
        for dim in dimensions:
            if dim <= 0:
                break
            self._number_of_dimensions += 1
        self._dimensions = tuple(dimensions[:self._number_of_dimensions])
        self._iter_pos = None
        if not self._number_of_dimensions:
            super().__init__()
            Multidimensional_array.increment()
            return
        try:
            iter(iterable)
        except TypeError:
            iterable = [iterable]
        iterable = list(iterable)
        if len(iterable) < dimensions[-1]:
            iterable += [fill for _ in range(dimensions[-1] - len(iterable))]
        numdim = self._number_of_dimensions - 1
        if numdim > 0:
            locked = Multidimensional_array._lock
            Multidimensional_array._lock = True
            sublists = [Multidimensional_array(dimensions[:-1], item, fill=fill)
                        for item in iterable[:dimensions[-1]]]
            Multidimensional_array._lock = locked
            Multidimensional_array.increment()
        else:
            sublists = iterable[:dimensions[-1]]
        super().__init__(sublists)

    def __getitem__(self, coordinates):
        """try:
            iter(coordinates)
        except TypeError:
            coordinates = [coordinates]
        coordinates = list(coordinates)
        if len(coordinates) < self._number_of_dimensions:
            coordinates += [slice(None) for _ in range(self._number_of_dimensions - len(coordinates))]
        elif len(coordinates) > self._number_of_dimensions:
            coordinates = coordinates[:self._number_of_dimensions]
        coordinates.reverse()"""
        coordinates = self._complete_coordinates(coordinates)
        coordinate = coordinates[0]
        if coordinate is None:
            coordinate = slice(None)
        if isinstance(coordinate, int):
            subarray = list.__getitem__(self, coordinate)
            return subarray[coordinates[1:]] if len(coordinates) > 1 else subarray
        if isinstance(coordinate, slice):
            sliced = list.__getitem__(self, coordinate)
            if len(coordinates) > 1:
                sliced = [subarray[coordinates[1:]] for subarray in sliced]
            try:
                dim = sliced[0].get_dimensions()
            except (IndexError, AttributeError):
                dim = ()
            return Multidimensional_array(dim + (len(sliced),), sliced, self._fill)
        raise TypeError('coordinates must be in form of tuple of integers, slices or None')

    def __setitem__(self, key, value):
        target = self[key]
        coordinates = self._complete_coordinates(key)
        if isinstance(target, Multidimensional_array) and target._ID == self._ID:
            if not isinstance(value, Multidimensional_array) or value.get_dimensions() != target.get_dimensions():
                raise TypeError('can only assign a Multidimensional_array of the same size as target')
            coordinates.reverse()
            for relative, item in value.enumerated:
                relative_iter = iter(relative)
                completed = coordinates.copy()
                for index, coordinate in enumerate(coordinates):
                    if isinstance(coordinate, slice):
                        completed[index] = range(coordinate.start if isinstance(coordinate.start, int) else 0,
                                                 coordinate.stop if isinstance(coordinate.stop, int) else
                                                 self.get_dimensions()[index], coordinate.step if
                                                 isinstance(coordinate.step, int) else 1)[next(relative_iter)]
                self[completed] = item
        else:
            subarray = self
            for coordinate in coordinates[:-1]:
                subarray = list.__getitem__(subarray, coordinate)
            list.__setitem__(subarray, coordinates[-1], value)

    def __iter__(self):
        self._iter_pos = [0] * self._number_of_dimensions
        self._stop = False
        return self

    def __next__(self):
        if self._stop:
            self._stop = False
            raise StopIteration
        item = self[self._iter_pos]
        for dimension in range(len(self._iter_pos)):
            self._iter_pos[dimension] += 1
            if self._iter_pos[dimension] == self.get_dimensions()[dimension]:
                self._iter_pos[dimension] = 0
            else:
                return item
        self._stop = True
        return item

    def _complete_coordinates(self, coordinates):
        try:
            iter(coordinates)
        except TypeError:
            coordinates = [coordinates]
        coordinates = list(coordinates)
        if len(coordinates) < self._number_of_dimensions:
            coordinates += [slice(None) for _ in range(self._number_of_dimensions - len(coordinates))]
        elif len(coordinates) > self._number_of_dimensions:
            coordinates = coordinates[:self._number_of_dimensions]
        coordinates.reverse()
        return coordinates

    def get_dimensions(self):
        return self._dimensions

    def copy(self):
        return Multidimensional_array(self.get_dimensions(), self.list(), self._fill)

    def list(self):
        return [list.__getitem__(self, i).list() if len(self.get_dimensions()) > 1 else list.__getitem__(self, i)
                for i in range(self.get_dimensions()[-1])]


if __name__ == "__main__":
    array = Multidimensional_array((4, 3), ['1234', 'abcd', Multidimensional_array((3,), 'AB', 'C')])
    print(array, end='\n\n')
    for j in range(array.get_dimensions()[1]):
        for i in range(array.get_dimensions()[0]):
            print(array[i, j], end='')
        print()
    print()
    for item in array:
        print(item)
    print()
    for item in array.enumerated:
        print(item)
    print('\n\n\n\n')
    array = Multidimensional_array((2, 2, 2, 2), [[[[1, 1], [1, 1]], [[1, 1], [1, 1]]], [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]])
    array1 = array.copy()
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    array1[a, b, c, d] = a + b + c + d
    print(array1, array, '', sep='\n')
    array = Multidimensional_array((5,), [0, 1, 2, 3, 4])
    array[0] = None
    array[1:4] = Multidimensional_array((3,), 'abc')
    print(array)
