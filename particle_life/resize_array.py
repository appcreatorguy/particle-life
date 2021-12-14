def resize_array(array, size, defaultValue):
    array.extend([defaultValue] * size)
    return array[:size]
