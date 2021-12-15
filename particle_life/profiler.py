import cProfile
from cProfile import *
import universe as uni

universe = uni.Universe(9, 400, 1280, 720)
universe.re_seed(-0.02, 0.06, 0.0, 20.0, 20.0, 70.0, 0.05, False)

cProfile.run('universe.step()')