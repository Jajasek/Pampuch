class Shared_data:
    instances = dict()

    def __init__(self, ID=0):
        object.__setattr__(self, 'ID', ID)
        if ID in self.instances:
            for name, value in self.instances[ID][0].__dict__.items():
                object.__setattr__(self, name, value)
            self.instances[ID].append(self)
        else:
            self.instances[ID] = [self]
            self.first_init()

    def first_init(self, *args, **kwargs):
        pass

    def update(self, key, old_value, new_value):
        pass

    def delete(self):
        self.instances.remove(self)

    def __setattr__(self, key, value, update=True):
        old = getattr(self, key, None)
        for instance in self.instances[self.ID]:
            object.__setattr__(instance, key, value)
        if update:
            self.update(key, old, value)
