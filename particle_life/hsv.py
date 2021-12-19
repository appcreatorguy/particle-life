from pygame import Color


def from_HSV(h, s, v):
    i = int(h * 6)
    f = h * 6 - i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)

    r = g = b = 0

    switch = i % 6  # value to pseudo-switch on as python has no native switch statement
    if switch == 0:
        r = v
        g = t
        b = p
    elif switch == 1:
        r = q
        g = v
        b = p
    elif switch == 2:
        r = p
        g = v
        b = t
    elif switch == 3:
        r = p
        g = q
        b = v
    elif switch == 4:
        r = t
        g = p
        b = v
    elif switch == 5:
        r = v
        g = p
        b = q

    return Color(int(r * 255), int(g * 255), int(b * 255), 255)
