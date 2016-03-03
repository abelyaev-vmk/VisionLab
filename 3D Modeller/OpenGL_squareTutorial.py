from math import sqrt, pi, sin, cos
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


def normalize(vect):
    norm = np.linalg.norm(vect)
    return vect / norm if norm > 0 else vect


def identity():
    return np.asarray([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], dtype=np.float32, order='F')


def model_view():
    mv = identity()
    mv = translate(mv, (0, -1, -1))
    mv = rotate(mv, (0, 0, 1), 50)
    return mv


def projection():
    return identity()


def translate(matrix, vec):
    matrix[3, :3] = vec[:]
    return matrix


def rotate(matrix, axis, angle):
    ## -angle ???
    from CommonFunctions import axis_rotation_matrix, matrix3to4
    return np.matrix(matrix) * matrix3to4(axis_rotation_matrix(axis, -angle * pi / 180.0))


class Renderer:
    def __init__(self, vertexes):
        self.vertexes = vertexes

    def __draw_objects(self):
        glBegin(GL_POLYGON)
        for vertex in self.vertexes:
            glNormal3f(0, 0, 1)
            glVertex3fv(vertex)
            glColor3f(1, 1, 1)
            # or glTexCoord2fv((x, y))
        glEnd()

    def __display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        # gluLookAt(self.eye[0], self.eye[1], self.eye[2],
        #           self.cen[0], self.cen[1], self.cen[2],
        #           self.up[0], self.up[1], self.up[2])
        # glTranslatef(0, 0, -2)
        glLoadMatrixf(model_view())
        # glRotatef(10, 1, 0, 0)
        self.__draw_objects()
        glutSwapBuffers()
        # print "INFO NOW"
        # print glGetFloatv(GL_PROJECTION_MATRIX)
        # print glGetFloatv(GL_MODELVIEW_MATRIX)
        #
        # exit(0)

    def __reshape(self, width, height):
        glViewport(0, 0, width, height)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)  # set projection matrix parameters
        glLoadIdentity()
        # glLoadMatrixf()
        gluPerspective(60.0, float(width) / float(height), 1.0, 60.0)
        # glMatrixMode(GL_MODELVIEW)  # set modelview matrix parameters
        # glLoadIdentity()
        # gluLookAt(self.eye[0], self.eye[1], self.eye[2],
        #           self.cen[0], self.cen[1], self.cen[2],
        #           self.up[0], self.up[1], self.up[2])

    def __init_opengl(self):
        # initialize parameters
        glClearColor(0, 0, 0, 0)
        self.eye, self.cen, self.up = [0, 0, 0], [0, 0, 0], [0, 1, 0]
        self.mouse_x, self.mouse_y, self.push = 0, 0, False

    def render(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE)
        glutInitWindowSize(700, 350)
        glutInitWindowPosition(50, 50)
        glutCreateWindow('Square Tutorial')
        glutDisplayFunc(self.__display)
        glutReshapeFunc(self.__reshape)
        glutKeyboardFunc(self.__keyboard)
        glutMouseFunc(self.__mouse)
        glutMotionFunc(self.__mouse_move)
        glutIdleFunc(glutPostRedisplay)
        self.__init_opengl()
        glutMainLoop()

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
        speed = 0.5
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
            if _y:
                self.cen[1] -= _y / 30.0
        self.mouse_x = pos_x
        self.mouse_y = pos_y


if __name__ == '__main__':
    vertexes = ((0, 0, 0), (0, 1, 0), (1, 1, 0), (1, 0, 0))
    rend = Renderer(vertexes)
    rend.render()
