from math import sqrt
import numpy as np
from matplotlib import pyplot as plt
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from triangle import delaunay

def line_length(line=((0, 0), (1, 1))):
    return sqrt((line[0][0] - line[1][0]) ** 2 +
                (line[0][1] - line[1][1]) ** 2)


def dist(point1, point2):
    return line_length([point1, point2])


def get_parameters(line=((0, 0), (1, 1))):
    x1, y1, x2, y2 = line[0] + line[1]
    a = (y2 - y1) / (x2 - x1)
    b = y1 - a * x1
    return a, b


def get_value(param=(1, 0), x=0):
    return param[0] * x + param[1]


def near_lines(line1, line2, steps=100, threshold_dist=25, threshold_prec=0.6):
    # line=((x1, y1), (x2, y2))
    point11, point12 = line1
    point21, point22 = line2
    if dist(point22, point11) < dist(point21, point11):
        point21, point22 = point22, point21
    step1 = [(point11[0] - point12[0]) / steps, (point11[1] - point12[1]) / steps]
    step2 = [(point21[0] - point22[0]) / steps, (point21[1] - point22[1]) / steps]
    near_steps = 0
    for i in range(steps):
        new_point1 = [point12[0] + i * step1[0], point12[1] + i * step1[1]]
        new_point2 = [point22[0] + i * step2[0], point22[1] + i * step2[1]]
        if dist(new_point1, new_point2) < threshold_dist:
            near_steps += 1
    return True if near_steps / steps >= threshold_prec else False


def triangle_square(p1, p2, p3):
    l1, l2, l3 = dist(p1, p2), dist(p2, p3), dist(p3, p1)
    pp = 0.5 * (l1 + l2 + l3)
    spp = pp * (pp - l1) * (pp - l2) * (pp - l3)
    return sqrt(spp) if spp > 0 else 0


def inside(lines, point, square=None):
    if not square:
        square = 0
        point_on_polygon = lines[0, 0]
        for line in lines:
            square += triangle_square(point_on_polygon, line[0], line[1])
    new_square = 0
    for line in lines:
        new_square += triangle_square(point, line[0], line[1])
    return False if abs(square - new_square) > 0.5 else True


def get_points_on_plane(lines, increase=2.0):
    min_x, min_y, max_x, max_y = 10000, 10000, 0, 0
    for line in lines:
        # lines[i][1] = lines[i+1][0]
        x, y = line[0]
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    shape = ((max_x - min_x) * int(increase), (max_y - min_y) * int(increase))
    rect = np.zeros(shape)
    square = 0
    point_on_polygon = lines[0][0]
    for line in lines:
        square += triangle_square(point_on_polygon, line[0], line[1])
    increase = float(increase)
    for i in range(shape[0]):
        for j in range(shape[1]):
            if inside(lines=lines, point=[i / increase + min_x, j / increase + min_y], square=square):
                rect[i, j] = 1
    return rect


def near_points(p1, p2):
    return True if abs(p1[0] - p2[0]) <= 1 and abs(p1[1] - p2[1]) <= 1 else False


def get_triangles_on_plane(plane, increase=2.0):
    triangles = []
    for i in range(plane.shape[0]):
        for j in range(plane.shape[1]):
            if not plane[i][j]:
                continue
            point = [i, j]
            points = []
            for i_ in range(max(0, i - 1), min(i + 1, plane.shape[0])):
                for j_ in range(max(0, j - 1), min(j + 1, plane.shape[1])):
                    pass

    return triangles


def get_vertex_name(pos):
    return str(pos[0]) + '_' + str(pos[1]) + '_' + str(pos[2])


class Vertex:
    def __init__(self, pos=(0, 0, 0), nor=(0, 0, 0), tex=(0, 0), col=(0, 0, 0)):
        self.pos = pos
        self.nor = nor
        self.tex = tex
        self.col = col
        self.id = get_vertex_name(self.pos)

    def __getitem__(self):
        return self


class VertexData:
    def __init__(self):
        self.vertexes_dict = {}
        self.vertexes_array = []

    def __add__(self, other):
        temp_data = self
        if other.__class__.__name__ == Vertex.__name__:
            if other.id not in self.vertexes_dict:
                temp_data.vertexes_dict[other.id] = other
        elif type(other) == list:
            v = Vertex(pos=other)
            if v.id not in self.vertexes_dict:
                temp_data.vertexes_dict[v.id] = v
        self.vertexes_array = map(lambda item: item[1], self.vertexes_dict.items())
        return temp_data

    def __iadd__(self, other):
        if other.__class__.__name__ == Vertex.__name__:
            if other.id not in self.vertexes_dict:
                self.vertexes_dict[other.id] = other
        elif type(other) == list:
            v = Vertex(pos=other)
            if v.id not in self.vertexes_dict:
                self.vertexes_dict[v.id] = v
        self.vertexes_array = map(lambda item: item[1], self.vertexes_dict.items())
        return self

    def __len__(self):
        return len(self.vertexes_dict)

    def __getitem__(self, item):
        if type(item) == int or type(item) == float or item.__class__.__name__ == 'int32':
            return self.vertexes_array[item]
        if item not in self.vertexes_dict:
            return None
        return self.vertexes_dict[item]

    def __contains__(self, item):
        return item in self.vertexes_dict

    def __iter__(self):
        for elem in self.vertexes_array:
            yield elem


class Renderer:
    def __init__(self, walls=(), ground=None, sky=None):
        self.walls = walls
        self.ground = ground
        self.sky = sky

        self.vertexes = VertexData()
        self.triangles = []
        self.count = 0

    def set_vertexes(self):
        self.set_ground(increase=1)
        for wall in self.walls:
            self.set_wall(wall=wall)
        self.set_sky()

    def set_ground(self, normal=(0, 0, 1), increase=2.0):
        if not self.ground:
            return
        increase = float(increase)
        # find max and min on ground
        points_on_plane = get_points_on_plane(self.ground, increase=increase)
        print points_on_plane
        pop = points_on_plane
        square = 0
        for i in range(pop.shape[0]):
            for j in range(pop.shape[1]):
                if pop[i][j]:
                    square += 1
                    self.vertexes += Vertex(pos=(int(i / increase), int(j / increase), 0),
                                            nor=normal, col=(1, 1, 1))
        print square
        if not self.triangles:
            self.set_triangles()
        # triangles = get_triangles_on_plane(points_on_plane, increase=2)
        # print len(triangles)
        # self.vertexes += triangles
        # self.normals += [normal for _ in xrange(len(triangles) / 3)]
        # self.colors += [(1, 1, 1) for _ in xrange(len(triangles))]

    def set_wall(self, wall=None, normal=(1, 0, 0)):
        pass

    def set_sky(self, normal=(0, -1, 0)):
        pass

    def set_triangles(self):
        points = []
        for ver in self.vertexes:
            points.append(ver.pos[0:2])
        triangles = delaunay(points)
        for tri in triangles:
            self.triangles.extend(self.vertexes[tri[i]].pos for i in xrange(3))
        print self.triangles

    def __draw_objects(self):
        glBegin(GL_POLYGON)
        # for i in xrange(self.count):
        #     glNormal3fv(self.normals[i])
        #     glVertex3fv(self.vertexes[i])
        #     glColor3fv(self.colors[i])
        from random import random
        for tri in self.triangles:
            glNormal3fv((0, 0, 1))
            glVertex3fv(tri)
            glColor3fv(self.vertexes[get_vertex_name(tri)].col)

        # for i in range(2, len(self.vertexes)):
        #     glNormal3fv(self.vertexes[i - 2].nor)
        #     glVertex3fv(self.vertexes[i - 2].pos)
        #     glColor3fv(self.vertexes[i - 2].col)
        #     glNormal3fv(self.vertexes[i - 1].nor)
        #     glVertex3fv(self.vertexes[i - 1].pos)
        #     glColor3fv(self.vertexes[i - 1].col)
        #     glNormal3fv(self.vertexes[i].nor)
        #     glVertex3fv(self.vertexes[i].pos)
        #     glColor3fv(self.vertexes[i].col)
        glEnd()

    @staticmethod
    def __init():
        glClearColor(0, 0, 0, 0)

    @staticmethod
    def __reshape(width, height):
        glViewport(0, 0, width, height)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, float(width) / float(height), 1.0, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0)

    def __display(self):
        glClear(GL_COLOR_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(0, 0, 0, 1, 1, 1, 0, 1, 0)
        glTranslatef(4, 4, 4)
        glRotatef(0, 1, -1, 0)
        d=3/sqrt(3)
        glTranslatef(d - 1.5, d - 1.5, d - 1.5)
        glTranslatef(1.5, 1.5, 1.5)  # move cube from the center
        glRotatef(0, 1.0, 1.0, 0.0)
        glTranslatef(-1.5, -1.5, -1.5)  # move cube into the center
        self.__draw_objects()
        glutSwapBuffers()

    def render(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
        glutInitWindowSize(500, 500)
        glutCreateWindow('First Try')
        glutDisplayFunc(self.__display)
        glutReshapeFunc(self.__reshape)
        self.__init()
        glutMainLoop()


if __name__ == '__main__':
    k = 2
    lines = map(lambda m: ((m[0][0] * k, m[0][1] * k), (m[1][0] * k, m[1][1] * k)),
                (((5, 5), (10, 2)), ((10, 2), (15, 7)), ((15, 7), (8, 20)), ((8, 20), (5, 5))))
    rend = Renderer(ground=lines)
    rend.set_vertexes()
    rend.render()
