from math import sqrt, pi, sin, cos
import numpy as np
from matplotlib import pyplot as plt
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from triangle import delaunay
from PIL import Image


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


def normalize(vect):
    norm = np.linalg.norm(vect)
    return vect / norm if norm > 0 else vect


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
    def __init__(self, walls=(), ground=None, sky=None, filename='SOURCE-2.jpg'):
        self.walls = walls
        self.ground = ground
        print ground
        self.sky = sky

        self.vertexes = VertexData()
        self.triangles = []
        self.count = 0

        self.filename = filename

    def set_vertexes(self, increase=2):
        # self.set_ground_by_points_in_grid(increase=1)
        self.set_ground_by_lines(increase=increase)
        # self.set_ground_by_vertexes()
        for wall in self.walls:
            self.set_wall(wall=wall)
        self.set_sky()

    def set_ground_by_lines(self, increase=4.0):
        if not self.ground:
            return
        tangents = [line[0][1] / line[0][0] for line in self.ground]
        idx_min_tg = tangents.index(min(tangents))
        points_count = len(self.ground)
        p1, p2 = self.ground[(idx_min_tg - 1) % points_count][0], \
                 self.ground[(idx_min_tg + 1) % points_count][0]
        next_idx = (idx_min_tg - 1) % points_count if p1[0] > p2[0] \
            else (idx_min_tg + 1) % points_count
        oriented_points = [self.ground[idx_min_tg][0], self.ground[next_idx][0]]
        now_idx, prev_idx = next_idx, idx_min_tg
        idx = self.find_next_point(now_idx=now_idx, prev_idx=prev_idx)
        while now_idx != idx_min_tg:
            print idx
            oriented_points.append(self.ground[idx][0])
            now_idx, prev_idx = idx, now_idx
            idx = self.find_next_point(now_idx=now_idx, prev_idx=prev_idx, count=points_count)
        print oriented_points

        orientations = [self.line_orientation(oriented_points[i], oriented_points[(i + 1) % points_count])
                        for i in range(points_count)]
        param = lambda indx: get_parameters((oriented_points[indx], oriented_points[(indx + 1) % points_count]))
        lines_func = [lambda x, y: y <= get_value(param(i), x) if orientations[i] > 0 else y >= get_value(param(i), x)
                      for i in range(points_count)]

        increase = float(increase)
        min_x, min_y, max_x, max_y = 10000, 10000, 0, 0
        for line in lines:
            x, y = line[0]
            min_x = min(min_x, x)
            min_y = min(min_y, y)
            max_x = max(max_x, x)
            max_y = max(max_y, y)
        square = 0

        x, x_m, y_m = 0, max_x - min_x, max_y - min_y
        while x < x_m:
            y = 0
            while y < y_m:
                if all(func(x, y) for func in lines_func):
                    square += 1
                    from random import random
                    self.vertexes += Vertex(pos=(int(x / increase), int(y / increase), 0),
                                            nor=(0, 0, 1), col=(random(), random(), random()))
                y += 1 / increase
            x += 1 / increase
        # for x in [0: 1/increase: max_x - min_x]:
        #     for y in range((max_y - min_y) * int(increase)):
        #         if all(func(x, y) for func in lines_func):
        #             square += 1
        #             from random import random
        #             self.vertexes += Vertex(pos=(int(x / increase), int(y / increase), 0),
        #                                     nor=(0, 0, 1), col=(random(), random(), random()))
        print square
        if not self.triangles:
            self.set_triangles()

    def set_ground_by_points_in_grid(self, normal=(0, 0, 1), increase=2.0):
        if not self.ground:
            return
        increase = float(increase)
        points_on_plane = get_points_on_plane(self.ground, increase=increase)
        print points_on_plane
        pop = points_on_plane
        square = 0
        for i in range(pop.shape[0]):
            for j in range(pop.shape[1]):
                if pop[i][j]:
                    square += 1
                    from random import random
                    self.vertexes += Vertex(pos=(int(i / increase), int(j / increase), 0),
                                            nor=normal, col=(random(), random(), random()))
        print square
        if not self.triangles:
            self.set_triangles()

    def __draw_ground_by_vertexes(self, source='SOURCE.jpg'):
        if not self.ground:
            return
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glBegin(GL_POLYGON)
        glNormal3f(0, 0, -1)
        mult = 0.5 * (self.image_height + self.image_width) / 100
        for line in self.ground:
            point_x, point_y = float(line[0][0]) / self.image_width, float(line[0][1]) / self.image_height
            glTexCoord2f(point_x, point_y)
            # glTexCoord2f(line[0][0], line[0][1])
            glVertex3f((point_x) * mult, point_y * mult, 0)
        glEnd()

    @staticmethod
    def find_next_point(now_idx=1, prev_idx=0, count=5):
        return (now_idx + 1 if prev_idx == (now_idx - 1) % count else now_idx - 1) % count

    @staticmethod
    def line_orientation(p1, p2):
        return 1 if p1[0] > p2[0] else -1

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

    def __draw_objects(self):
        # glBegin(GL_POLYGON)
        # for i in xrange(self.count):
        #     glNormal3fv(self.normals[i])
        #     glVertex3fv(self.vertexes[i])
        #     glColor3fv(self.colors[i])
        from random import random
        # for tri in self.triangles:
        #     glNormal3fv((0, 0, 1))
        #     glVertex3fv(tri)
        #     glColor3fv(self.vertexes[get_vertex_name(tri)].col)

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
        # glEnd()
        x1, x2, y1, y2, z1, z2 = 0, 1, 0, 1, 0, 1
        glBegin(GL_POLYGON)  # front face
        glNormal3f(0.0, 0.0, 1.0)
        glTexCoord2f(0, 0)
        glVertex3f(x1, y1, z2)
        glTexCoord2f(1, 0)
        glVertex3f(x2, y1, z2)
        glTexCoord2f(1, 1)
        glVertex3f(x2, y2, z2)
        glTexCoord2f(0, 1)
        glVertex3f(x1, y2, z2)
        glEnd()

        glBegin(GL_POLYGON)  # back face
        glNormal3f(0.0, 0.0, -1.0)
        glTexCoord2f(1, 0)
        glVertex3f(x2, y1, z1)
        glTexCoord2f(0, 0)
        glVertex3f(x1, y1, z1)
        glTexCoord2f(0, 1)
        glVertex3f(x1, y2, z1)
        glTexCoord2f(1, 1)
        glVertex3f(x2, y2, z1)
        glEnd()

        glBegin(GL_POLYGON)  # left face
        glNormal3f(-1.0, 0.0, 0.0)
        glTexCoord2f(0, 0)
        glVertex3f(x1, y1, z1)
        glTexCoord2f(0, 1)
        glVertex3f(x1, y1, z2)
        glTexCoord2f(1, 1)
        glVertex3f(x1, y2, z2)
        glTexCoord2f(1, 0)
        glVertex3f(x1, y2, z1)
        glEnd()

        glBegin(GL_POLYGON)  # right face
        glNormal3f(1.0, 0.0, 0.0)
        glTexCoord2f(0, 1)
        glVertex3f(x2, y1, z2)
        glTexCoord2f(0, 0)
        glVertex3f(x2, y1, z1)
        glTexCoord2f(1, 0)
        glVertex3f(x2, y2, z1)
        glTexCoord2f(1, 1)
        glVertex3f(x2, y2, z2)
        glEnd()

        glBegin(GL_POLYGON)  # top face
        glNormal3f(0.0, 1.0, 0.0)
        glTexCoord2f(0, 1)
        glVertex3f(x1, y2, z2)
        glTexCoord2f(1, 1)
        glVertex3f(x2, y2, z2)
        glTexCoord2f(1, 0)
        glVertex3f(x2, y2, z1)
        glTexCoord2f(0, 0)
        glVertex3f(x1, y2, z1)
        glEnd()

        glBegin(GL_POLYGON)  # bottom face
        glNormal3f(0.0, -1.0, 0.0)
        glTexCoord2f(1, 1)
        glVertex3f(x2, y1, z2)
        glTexCoord2f(1, 0)
        glVertex3f(x1, y1, z2)
        glTexCoord2f(0, 0)
        glVertex3f(x1, y1, z1)
        glTexCoord2f(0, 1)
        glVertex3f(x2, y1, z1)
        glEnd()

    @staticmethod
    def __draw_coordinates():
        glLineWidth(2)
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(10, 0, 0)
        glEnd()

        glLineWidth(2)
        glColor3f(0, 1, 0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 10, 0)
        glEnd()

        glLineWidth(2)
        glColor3f(0, 0, 1)
        glBegin(GL_LINES)

        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 10)
        glEnd()

    def loadTexture(self, filename='SOURCE.jpg'):
        print filename
        image = Image.open(filename)
        self.image_width = image.size[0]
        self.image_height = image.size[1]
        image = image.tobytes('raw', 'RGBA', 0, -1)
        texture = glGenTextures(1)

        glBindTexture(GL_TEXTURE_2D, texture)  # 2d texture (x and y size)
        glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
        gluBuild2DMipmaps(GL_TEXTURE_2D, 3, self.image_width, self.image_height, GL_RGBA, GL_UNSIGNED_BYTE, image)
        self.texture = texture

    def __init(self):
        glClearColor(0, 0, 0, 0)
        glClearDepth(1.0)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        self.eye, self.cen, self.up = [0, 0, 5], [3, 3, 0], [0, 1, 1]
        self.mouse_x, self.mouse_y, self.push = 0, 0, False
        self.loadTexture(filename=self.filename)
        gluPerspective(60, 1.5, 0.1, 100000)

    def __reshape(self, width, height):
        glViewport(0, 0, width, height)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, float(width) / float(height), 1.0, 60.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.eye[0], self.eye[1], self.eye[2],
                  self.cen[0], self.cen[1], self.cen[2],
                  self.up[0], self.up[1], self.up[2])
        print self.eye, self.cen

    def __display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.eye[0], self.eye[1], self.eye[2],
                  self.cen[0], self.cen[1], self.cen[2],
                  self.up[0], self.up[1], self.up[2])
        # glLoadIdentity()
        # glTranslatef(1, 0, 3)
        # glRotatef(0, 1, -1, 0)
        # d = 3 / sqrt(3)
        # glTranslatef(d - 1.5, d - 1.5, d - 1.5)
        # glTranslatef(1.5, 1.5, 1.5)  # move cube from the center
        # glRotatef(0, 1.0, 1.0, 0.0)
        # glTranslatef(-1.5, -1.5, -1.5)  # move cube into the center
        # self.__draw_objects()
        self.__draw_ground_by_vertexes()
        self.__draw_coordinates()
        glutSwapBuffers()

    def __e_pressed(self, speed):
        temp = map(lambda a, b: (a - b) * speed / 3.0, self.cen, self.eye)
        self.eye = map(lambda a, t: a + t, self.eye, temp)
        self.cen = map(lambda a, t: a + t, self.cen, temp)

    def __q_pressed(self, speed):
        temp = map(lambda a, b: (a - b) * speed / 3.0, self.cen, self.eye)
        self.eye = map(lambda a, t: a - t, self.eye, temp)
        self.cen = map(lambda a, t: a - t, self.cen, temp)

    def __w_pressed(self, speed):
        self.eye[1] += 3 * speed
        self.cen[1] += 3 * speed

    def __s_pressed(self, speed):
        self.eye[1] -= 3 * speed
        self.cen[1] -= 3 * speed

    def __a_pressed(self, speed):
        cross_vector = normalize(np.cross(np.array(map(lambda a, b: a - b, self.eye, self.cen)),
                                          np.array(self.up)))
        self.eye = map(lambda a, b: a + b * speed, self.eye, cross_vector)
        self.cen = map(lambda a, b: a + b * speed, self.cen, cross_vector)

    def __d_pressed(self, speed):
        cross_vector = normalize(np.cross(np.array(map(lambda a, b: a - b, self.eye, self.cen)),
                                          np.array(self.up)))
        self.eye = map(lambda a, b: a - b * speed, self.eye, cross_vector)
        self.cen = map(lambda a, b: a - b * speed, self.cen, cross_vector)

    def __keyboard(self, key, mx, my):
        speed = 0.8
        print self.cen, self.eye
        {
            'e': self.__e_pressed,
            'q': self.__q_pressed,
            'w': self.__w_pressed,
            'a': self.__a_pressed,
            's': self.__s_pressed,
            'd': self.__d_pressed,
        }[key](speed)

    def __mouse(self, button, mode, pos_x, pos_y):
        if button == GLUT_LEFT_BUTTON:
            self.mouse_x = pos_x
            self.mouse_y = pos_y
            self.push = True if mode == GLUT_DOWN else False

    def __mouse_move(self, pos_x, pos_y):
        if self.push:
            _x, _y = pos_x - self.mouse_x, pos_y - self.mouse_y
            temp = map(lambda a, b: a - b, self.cen, self.eye)
            if _x:
                fx = _x * pi / 180.0 / 10.0
                self.cen[2] = self.eye[2] + sin(fx) * temp[0] + cos(fx) * temp[2]
                self.cen[0] = self.eye[0] + cos(fx) * temp[0] - sin(fx) * temp[2]
            print _x, _y
            if _y:
                self.cen[1] -= _y / 10.0
        self.mouse_x = pos_x
        self.mouse_y = pos_y

    def render(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(500, 500)
        glutCreateWindow('First Try')
        glutDisplayFunc(self.__display)
        glutReshapeFunc(self.__reshape)
        glutKeyboardFunc(self.__keyboard)
        glutMouseFunc(self.__mouse)
        glutMotionFunc(self.__mouse_move)
        glutIdleFunc(glutPostRedisplay)
        self.__init()
        glutMainLoop()


def make_lines(points):
    lines = []
    for i in range(len(points)):
        line = [points[i], points[(i + 1) % len(points)]]
        lines.append(line)
    return lines


if __name__ == '__main__':
    k = 2
    # lines = map(lambda m: ((m[0][0] * k, m[0][1] * k), (m[1][0] * k, m[1][1] * k)),
    #             (((5, 5), (10, 2)), ((10, 2), (15, 7)), ((15, 7), (8, 20)), ((8, 20), (5, 5))))
    points = ((5, 5), (16, 7), (18, 20), (10, 25), (4, 20), (1, 10))
    lines = make_lines(points)
    rend = Renderer(ground=lines, filename='SOURCE-2.jpg')
    # rend.set_vertexes(increase=4)
    rend.render()
