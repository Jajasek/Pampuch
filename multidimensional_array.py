class Multidimensional_array(list):
    def __init__(self, dimensions=(1, 1), iterable=None, fill=None):
        self._fill = fill
        self.number_of_dimensions = 0
        for dim in dimensions:
            if dim <= 0:
                break
            self.number_of_dimensions += 1
        self.dimensions = dimensions[:self.number_of_dimensions]
        if not self.number_of_dimensions:
            super().__init__()
            return
        try:
            iter(iterable)
        except TypeError:
            iterable = [iterable]
        if len(iterable) < dimensions[0]:
            iterable += [fill for _ in range(dimensions[0] - len(iterable))]
        numdim = self.number_of_dimensions - 1
        if numdim > 0:
            sublist = [Multidimensional_array(dimensions[1:], item, fill=fill)
                       for item in iterable[:dimensions[0]]]
        else:
            sublist = iterable[:dimensions[0]]
        super().__init__(sublist)

    def __getitem__(self, item):
        if item is None:
            item = slice(None)
        if isinstance(item, int):
            return list.__getitem__(self, item)
        if isinstance(item, slice):
            sliced = list.__getitem__(self, item)
            return Multidimensional_array((len(sliced),) + self.dimensions[1:], sliced,
                                          self._fill)
        try:
            coordinate = item[0]
        except TypeError:
            pass
        else:
            if coordinate is None:
                item = (slice(None),) + item[1:]
            if isinstance(item[0], int):
                return self[item[0]][item[1:] if len(item) > 2 else item[1]]
            if isinstance(item[0], slice):
                sliced = list.__getitem__(self, item[0])
                sliced = [subarray[item[1:] if len(item) > 2 else item[1]] for subarray in sliced]
                try:
                    dim = sliced[0].dimensions
                except (IndexError, AttributeError):
                    dim = ()
                return Multidimensional_array((len(sliced),) + dim, sliced,
                                              self._fill)
        raise TypeError('coordinates must be in form of tuple of integers, slices or None')


if __name__ == "__main__":
    array = Multidimensional_array((3, 4), ['1234', 'abcd', 'ABCD'])
    print(array[None, None])
