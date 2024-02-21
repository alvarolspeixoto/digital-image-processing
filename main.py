import os
from ImageOperations import *

io = ImageOperations()

current_path = os.getcwd()

file_path = os.path.join(current_path, "figuras-originais", "barco.pgm")

new_path = os.path.join(current_path, "figuras-salvas", "barco-desfocado-1.pgm")

# Distância até a borda
n = 1
io.smoothing_filter(file_path, new_path, n)