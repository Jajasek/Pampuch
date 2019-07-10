class FileFormatError(Exception):
    def __init__(self, message='', level_index=None):
        self.message = message
        self.level_index = level_index
