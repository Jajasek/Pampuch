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
    def __init__(self, dimensions=(1, 1), iterable=None, fill=None):
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
            return
        try:
            iter(iterable)
        except TypeError:
            iterable = [iterable]
        if len(iterable) < dimensions[-1]:
            iterable += [fill for _ in range(dimensions[-1] - len(iterable))]
        numdim = self._number_of_dimensions - 1
        if numdim > 0:
            sublists = [Multidimensional_array(dimensions[:-1], item, fill=fill)
                        for item in iterable[:dimensions[-1]]]
        else:
            sublists = iterable[:dimensions[-1]]
        super().__init__(sublists)

    def __getitem__(self, coordinates):
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

    def get_dimensions(self):
        return self._dimensions


if __name__ == "__main__":
    array = Multidimensional_array((4, 3), ['1234', 'abcd', 'ABCD'])
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
