from math import sqrt, pi, sin, cos
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from PIL import Image
from CameraProperties import CameraProperties
from ExtendedImage import ExtendedImage


def normalize(vect):
    norm = np.linalg.norm(vect)
    return vect / norm if norm > 0 else vect


def make_lines(points):
    lines = []
    for i in range(len(points)):
        line = [points[i], points[(i + 1) % len(points)]]
        lines.append(line)
    return lines


class Renderer:
    def __init__(self, project='SOURCE', ground=None, walls=(), sky=None, reducing=1):
        self.walls = walls
        self.ground = ground
        self.sky = sky

        self.project = project
        self.cp = CameraProperties(project=self.project)
        self.reducing = reducing
        self.get_ground_image()
        self.ground_image.show()

    def get_ground_image(self):
        self.ground_image = ExtendedImage.load(self.project, key='ground')
        if not self.ground_image:
            self.ground_image = self.cp.image2plane(reducing=self.reducing, plane=(0, 0, 1, 0))

    def __load_ground_texture(self):
        image = self.ground_image.image
        width, height = image.size
        try:
            image = image.tobytes('raw', 'RGB', 0, -1)
            texture = glGenTextures(1)

            glBindTexture(GL_TEXTURE_2D, texture)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            gluBuild2DMipmaps(GL_TEXTURE_2D, 3, width, height, GL_RGB, GL_UNSIGNED_BYTE, image)
            self.ground_texture = texture
        except SystemError:
            image = image.tobytes('raw', 'RGBA', 0, -1)
            texture = glGenTextures(1)

            glBindTexture(GL_TEXTURE_2D, texture)
            glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
            gluBuild2DMipmaps(GL_TEXTURE_2D, 3, width, height, GL_RGBA, GL_UNSIGNED_BYTE, image)
            self.ground_texture = texture

    def __draw_ground(self):
        if not self.ground:
            return
        glColor3f(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self.ground_texture)
        glBegin(GL_POLYGON)
        glNormal3f(0, 0, 1)
        count = 0
        for line in self.ground:
            if count > self.max_count:
                break
            count += 1
            _x, _y = line[0]
            wp = self.cp.img2world(point=(_x, _y), plane=(0, 0, 1, 0), reducing=self.reducing)
            # tex_coord = self.ground_image.image_coordinates(wp)
            # print tex_coord
            # width, height = self.ground_image.image.size
            # glTexCoord2f(wp[0] / width, wp[1] / height)
            # tex_coord = map(lambda a, b: a / b,
            #                   self.ground_image.image_coordinates(wp),
            #                   self.ground_image.size())
            # if count == self.max_count:
            #     # print wp
            #     # print self.ground_image.image.size
            #     print self.ground_image.shape_reducing, self.ground_image.image.size
            #     print self.ground_image.offset_x, self.ground_image.offset_y
            #     print tex_coord, '\n'
            tex_coord = self.ground_image.texture_coordinates(wp[:2])
            if count == self.max_count:
                print tex_coord
            glTexCoord2fv(tex_coord)
            glVertex3f(float(wp[0]), float(wp[1]), 0)
        glEnd()

    def help_output(self):
        for line in self.ground:
            _x, _y = line[0]
            wp = self.cp.img2world(point=(_x, _y), plane=(0, 0, 1, 0), reducing=self.reducing)
            ip = self.cp.world2img(point=wp, reducing=self.reducing)
            tex_coord = self.ground_image.texture_coordinates(wp[:2])
            print (_x, _y), '->', wp, '->', ip
            print '->', tex_coord
            print '->', map(lambda a, b: a * b, tex_coord, self.ground_image.texture_size), '\n'
        exit()

    def __init(self):
        glClearColor(0, 0, 0, 0)
        glClearDepth(1.0)
        glDepthFunc(GL_LEQUAL)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_TEXTURE_2D)
        glHint(GL_POLYGON_SMOOTH_HINT, GL_NICEST)
        glHint(GL_PERSPECTIVE_CORRECTION_HINT, GL_NICEST)
        # self.eye, self.cen, self.up, self.right = [0, 0, 5], [3, 3, 0], [0, 1, 1], [1, 0, 0]
        self.eye, self.cen, self.up, self.right = self.cp.get_eye_center_up_right(reducing=self.reducing)
        self.mouse_x, self.mouse_y, self.push = 0, 0, False
        self.__load_ground_texture()
        glDisable(GL_TEXTURE_2D)
        glEnable(GL_TEXTURE_2D)
        self.max_count = 0
        # self.help_output()

    def __reshape(self, width, height):
        glViewport(0, 0, width, height)
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(60.0, float(width) / float(height), 1.0, 1000.0)
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
        self.__draw_coordinates()
        self.__draw_ground()
        glutSwapBuffers()

    @staticmethod
    def __draw_coordinates():
        glLineWidth(2)
        glColor3f(1, 0, 0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(1000, 0, 0)
        glEnd()

        glLineWidth(2)
        glColor3f(0, 1, 0)
        glBegin(GL_LINES)
        glVertex3f(0, 0, 0)
        glVertex3f(0, 1000, 0)
        glEnd()

        glLineWidth(2)
        glColor3f(0, 0, 1)
        glBegin(GL_LINES)

        glVertex3f(0, 0, 0)
        glVertex3f(0, 0, 1000)
        glEnd()

    def __e_pressed(self, speed):
        temp = map(lambda a, b: (a - b) * speed / 6.0, self.cen, self.eye)
        self.eye = map(lambda a, t: a + t, self.eye, temp)
        self.cen = map(lambda a, t: a + t, self.cen, temp)

    def __q_pressed(self, speed):
        temp = map(lambda a, b: (a - b) * speed / 6.0, self.cen, self.eye)
        self.eye = map(lambda a, t: a - t, self.eye, temp)
        self.cen = map(lambda a, t: a - t, self.cen, temp)

    def __w_pressed(self, speed):
        # self.eye[2] += 3 * speed
        # self.cen[2] += 3 * speed
        self.eye = map(lambda a, b: a + 3 * b, self.eye, self.up)
        self.cen = map(lambda a, b: a + 3 * b, self.cen, self.up)

    def __s_pressed(self, speed):
        # self.eye[2] -= 3 * speed
        # self.cen[2] -= 3 * speed
        self.eye = map(lambda a, b: a - 3 * b, self.eye, self.up)
        self.cen = map(lambda a, b: a - 3 * b, self.cen, self.up)

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

    def __look_up(self, speed):
        s_angle = sin(speed * 5 * pi / 180)
        self.cen = map(lambda a, b: a + b * s_angle, self.cen, np.cross(self.cen, self.right))
        self.up = map(lambda a, b: a + b * s_angle, self.up, np.cross(self.up, self.right))

    def __look_down(self, speed):
        s_angle = sin(speed * 5 * pi / 180)
        self.cen = map(lambda a, b: a - b * s_angle, self.cen, np.cross(self.cen, self.right))
        self.up = map(lambda a, b: a - b * s_angle, self.up, np.cross(self.up, self.right))

    def __look_left(self, speed):
        s_angle = sin(speed * 5 * pi / 180)
        self.cen = map(lambda a, b: a + b * s_angle, self.cen, np.cross(self.cen, self.up))
        self.right = map(lambda a, b: a + b * s_angle, self.right, np.cross(self.right, self.up))

    def __look_right(self, speed):
        s_angle = sin(speed * 5 * pi / 180)
        self.cen = map(lambda a, b: a - b * s_angle, self.cen, np.cross(self.cen, self.up))
        self.right = map(lambda a, b: a - b * s_angle, self.right, np.cross(self.right, self.up))

    def __increase_max_count(self, _):
        self.max_count += 1

    def __decrease_max_count(self, _):
        self.max_count -= 1

    def __keyboard(self, key, mx, my):
        speed = 0.8
        print self.cen, self.eye
        try:
            {
                'e': self.__e_pressed,
                'q': self.__q_pressed,
                'w': self.__w_pressed,
                'a': self.__a_pressed,
                's': self.__s_pressed,
                'd': self.__d_pressed,
                'i': self.__look_up,
                'k': self.__look_down,
                'j': self.__look_left,
                'l': self.__look_right,
                'x': self.__increase_max_count,
                'z': self.__decrease_max_count,
            }[key](speed)
        except KeyError:
            return

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
                fx = _x * pi / 180.0 / 20.0
                self.cen[2] = self.eye[2] + sin(fx) * temp[0] + cos(fx) * temp[2]
                self.cen[0] = self.eye[0] + cos(fx) * temp[0] - sin(fx) * temp[2]
            print _x, _y
            if _y:
                self.cen[1] -= _y / 20.0
        self.mouse_x = pos_x
        self.mouse_y = pos_y

    def render(self):
        glutInit(sys.argv)
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(1024, 720)
        glutCreateWindow('First Try')
        glutDisplayFunc(self.__display)
        glutReshapeFunc(self.__reshape)
        glutKeyboardFunc(self.__keyboard)
        glutMouseFunc(self.__mouse)
        glutMotionFunc(self.__mouse_move)
        glutIdleFunc(glutPostRedisplay)
        self.__init()
        glutMainLoop()


if __name__ == '__main__':
    rend = Renderer(project='SOURCE-2')
    rend.render()
