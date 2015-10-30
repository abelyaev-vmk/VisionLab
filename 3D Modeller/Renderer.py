from math import sqrt
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from ImageProperties import ImageProperties, \
    CameraProperties, RectProperties


def line_length(line=((0, 0), (1, 1))):
    return sqrt((line[0][0] - line[1][0]) ** 2 +
                (line[0][1] - line[1][1]) ** 2)


def get_parameters(line=((0, 0), (1, 1))):
    x1, y1, x2, y2 = line[0] + line[1]
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return a, b


def get_value(param=(1, 0), x=0):
    return param[0] * x + param[1]


def compare_lines(main_line, temp_line, steps=100):
    if line_length(main_line) < line_length(temp_line):
        main_line, temp_line = temp_line, main_line
    main_param, temp_param = get_parameters(main_line), get_parameters(temp_line)
    main_ort_param = (1 / main_param[0], temp_line[0][1] - temp_line[0][0] / main_param[0])



class Renderer:
    def __init__(self, ip=ImageProperties(),
                cp=CameraProperties(), rp=RectProperties()):
        self.ip = ip
        self.cp = cp
        self.rp = rp

    def set_data(self):
        print 'One wall data'
        pass
