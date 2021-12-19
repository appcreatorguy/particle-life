import particles

def resize_array(array, size, defaultValue):
    # Extend array to original size + final size, then cut to final size
    for i in range(size):
        array.append(defaultValue)
    return array[:size]

def make_particles(array, size):
    # Extend array to original size + final size, then cut to final size
    for i in range(size):
        array.append(particles.Particle())
    return array[:size]


def resize_2d_array(array, size, defaultValue):
    # Extend existing rows
    for i in range(len(array)):
        array[i] = resize_array(array[i], size, defaultValue)

    array.extend([[defaultValue] * size] * size)
    return array[:size]
