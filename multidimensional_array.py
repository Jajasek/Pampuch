class Points_iterator:
    def __init__(self, array):
        self.array = array
        self._stop = False
        self._iter_pos = None

    def __iter__(self):
        self._iter_pos = [0] * self.array._number_of_dimensions
        self._stop = False
        return self

    def __next__(self):
        if self._stop:
            self._stop = False
            raise StopIteration
        item = self.array[self._iter_pos]
        for dimension in range(self.array._number_of_dimensions):
            self._iter_pos[dimension] += 1
            if self._iter_pos[dimension] == self.array.get_dimensions()[dimension]:
                self._iter_pos[dimension] = 0
            else:
                return item
        self._stop = True
        return item


class Enumerated_iterator:
    def __init__(self, array):
        self.array = array

    def __iter__(self):
        self.array.points.__iter__()
        return self

    def __next__(self):
        pos = tuple(self.array.points._iter_pos)
        return pos, self.array.points.__next__()


class ID_generator:
    def __init__(self):
        self._lock = list()

    def __str__(self):
        return f'{id(self)}; {self._last_ID}; {self._lock}'

    def next(self):
        # print(f'ID_generator.next(): {id(self)}')
        if len(self._lock):
            return self._lock[-1]
        self._last_ID += 1
        return self._last_ID

    def lock(self, ID):
        self._lock.append(ID)

    def unlock(self):
        del self._lock[-1]

    @property
    def _last_ID(self):
        global last_ID_tmp
        # print(f'returning last ID: {id(self)}; {last_ID_tmp}')
        return last_ID_tmp

    @_last_ID.setter
    def _last_ID(self, value):
        global last_ID_tmp
        # print(f'changing last ID: {id(self)}; {last_ID_tmp}; {value}')
        last_ID_tmp = value


class Multidimensional_array:
    # ID = ID_generator()
    _last_ID = -1
    _lock = list()

    @classmethod
    def next_ID(cls):
        if len(cls._lock):
            return cls._lock[-1]
        cls._last_ID += 1
        return cls._last_ID

    @classmethod
    def lock_ID(cls, ID):
        cls._lock.append(ID)

    @classmethod
    def unlock_ID(cls):
        del cls._lock[-1]

    def __init__(self, dimensions=(1, 1), iterable=None, fill=None):
        if iterable is None:
            iterable = list()

        # self.ID = Multidimensional_array.ID
        # self._ID = self.ID.next()
        self._ID = Multidimensional_array.next_ID()

        self.enumerated = Enumerated_iterator(self)
        self.points = Points_iterator(self)
        self._fill = fill
        self._number_of_dimensions = 0
        for dim in dimensions:
            if dim <= 0:
                break
            self._number_of_dimensions += 1
        self._dimensions = tuple(dimensions[:self._number_of_dimensions])
        if not self._number_of_dimensions:
            # super().__init__()
            self.values = list()
            return
        try:
            iter(iterable)
        except TypeError:
            iterable = [iterable]
        if isinstance(iterable, Multidimensional_array):
            # iterable = [list.__getitem__(iterable, i) for i in range(iterable.get_dimensions()[-1])]
            iterable = iterable.values.copy()
        else:
            iterable = list(iterable)
        if len(iterable) < dimensions[-1]:
            iterable += [fill for _ in range(dimensions[-1] - len(iterable))]
        numdim = self._number_of_dimensions - 1
        if numdim > 0:
            Multidimensional_array.lock_ID(self._ID)
            sublists = [Multidimensional_array(dimensions[:-1], item, fill=fill)
                        for item in iterable[:dimensions[-1]]]
            Multidimensional_array.unlock_ID()
        else:
            sublists = iterable[:dimensions[-1]]
        # super().__init__()
        # self += sublists
        self.values = sublists

    def __str__(self):
        return str(self.values)

    def __repr__(self):
        return str(self)

    def __getitem__(self, coordinates):
        # x coordinate is deepest in the list structure
        coordinates = self._complete_coordinates(coordinates)
        coordinate = coordinates[0]
        if coordinate is None:
            coordinate = slice(None)
        if isinstance(coordinate, int):
            # subarray = list.__getitem__(self, coordinate)
            subarray = self.values[coordinate]

            coordinates.reverse()
            return subarray[coordinates[:-1]] if len(coordinates) > 1 else subarray
        if isinstance(coordinate, slice):
            # sliced = list.__getitem__(self, coordinate)
            sliced = self.values[coordinate]

            if len(coordinates) > 1:
                coordinates.reverse()
                sliced = [subarray[coordinates[:-1]] for subarray in sliced]
            try:
                dim = sliced[0].get_dimensions()
            except (IndexError, AttributeError):
                dim = ()
            out = Multidimensional_array(dim + (len(sliced),), sliced, self._fill)
            out._ID = self._ID
            return out
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
                    if coordinate is None:
                        coordinate = slice(None)
                    if isinstance(coordinate, slice):
                        completed[index] = range(coordinate.start if isinstance(coordinate.start, int) else 0,
                                                 coordinate.stop if isinstance(coordinate.stop, int) else
                                                 self.get_dimensions()[index], coordinate.step if
                                                 isinstance(coordinate.step, int) else 1)[next(relative_iter)]
                self[completed] = item
        else:
            subarray = self
            for coordinate in coordinates[:-1]:
                # subarray = list.__getitem__(subarray, coordinate)
                subarray = subarray.values[coordinate]
            # list.__setitem__(subarray, coordinates[-1], value)
            subarray.values[coordinates[-1]] = value

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
        # return [list.__getitem__(self, i).list() if len(self.get_dimensions()) > 1 else list.__getitem__(self, i)
        #         for i in range(self.get_dimensions()[-1])]
        return [self.values[i].list() if len(self.get_dimensions()) > 1 else self.values[i]
                for i in range(self.get_dimensions()[-1])]

    def print(self):
        if len(self._dimensions) == 2:
            for j in range(self.get_dimensions()[1]):
                for i in range(self.get_dimensions()[0]):
                    print(self[i, j], end='')
                print()
            print()
        else:
            print(str(self))

    def count(self, object):
        count = 0
        for item in self.points:
            if object == item:
                count += 1
        return count


if __name__ == "__main__":
    array = Multidimensional_array((4, 3), ['1234', 'abcd', Multidimensional_array((3,), 'AB', 'C')])
    print(array, end='\n\n')
    for j in range(array.get_dimensions()[1]):
        for i in range(array.get_dimensions()[0]):
            print(array[i, j], end='')
        print()
    print()
    for item in array.points:
        print(item)
    print()
    for item in array.enumerated:
        print(item)
    print('\n\n\n\n')
    array = Multidimensional_array((2, 2, 2, 2), [[[[1, 1], [1, 1]], [[1, 1], [1, 1]]], [[[1, 1], [1, 1]], [[1, 1], [1, 1]]]])
    array1 = array.copy()
    print(array == array1, array is array1)
    for a in range(2):
        for b in range(2):
            for c in range(2):
                for d in range(2):
                    array1[a, b, c, d] = f'{a}{b}{c}{d}'
    print(array1, array, '', sep='\n')
    array = Multidimensional_array((5,), [0, 1, 2, 3, 4])
    array[0] = None
    array[1:4] = Multidimensional_array((3,), 'abc')
    print(array)
