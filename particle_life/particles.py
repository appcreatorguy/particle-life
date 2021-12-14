from resize_array import resize_array


def make_particle(x=0, y=0, vx=0, vy=0, particle_type=0):
    return {"x": x, "y": y, "vx": vx, "vy": vy, "type": particle_type}


class ParticleTypes:
    def __init__(self, size=0):
        self.col = [{"r": 0, "g": 0, "b": 0, "a": 0}] * size
        self.attract = [0] * (size * size)
        self.minR = [0] * (size * size)
        self.maxR = [0] * (size * size)

    def resize(self, size):
        resize_array(self.col, size, {"r": 0, "g": 0, "b": 0, "a": 0})
        resize_array(self.attract, size * size, 0)
        resize_array(self.minR, size * size, 0)
        resize_array(self.maxR, size * size, 0)

    def size(self):
        return len(self.col)

    def get_color(self, i):
        return self.col[i]

    def set_color(self, i, value):
        self.col[i] = value

    def get_attract(self, i, j):
        return self.attract[i * len(self.col) + j]

    def set_attract(self, i, j, value):
        self.attract[i * len(self.col) + j] = value

    def get_minR(self, i, j):
        return self.minR[i * len(self.col) + j]

    def set_minR(self, i, j, value):
        self.minR[i * len(self.col) + j] = value

    def get_maxR(self, i, j):
        return self.attract[i * len(self.col) + j]

    def set_maxR(self, i, j, value):
        self.maxR[i * len(self.col) + j] = value
