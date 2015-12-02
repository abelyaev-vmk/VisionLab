from math import sqrt, pi, sin, cos
import numpy as np
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
# from PIL import Image
from CameraProperties import CameraProperties
# from ExtendedImage import ExtendedImage
from Image3D import Image3D
from CommonFunctions import normalize, make_lines, dist


class Renderer:
    def __init__(self, project='SOURCE', ground=None, walls=(), sky=None, reducing=1):
        self.walls = walls
        self.ground = ground
        self.sky = sky
        self.reducing = reducing
        self.project = project
        self.cp = CameraProperties(project=self.project)
        self.ground_plane = (0, 0, 1, 0)
        self.walls_planes = [self.define_wall_plane(wall) for wall in walls]
        self.get_ground_image()
        self.get_walls_images()

    def get_ground_image(self):
        self.ground_image = Image3D.load(self.project, key='ground')
        if not self.ground_image:
            self.ground_image = self.cp.image2plane_2(reducing=self.reducing,
                                                      plane=self.ground_plane,
                                                      lines=self.ground)

    def define_wall_plane(self, wall):
        points = []
        for line in wall:
            points.append(line[0])
        distances = np.zeros((len(points), len(self.ground)))
        for p, point in enumerate(points):
            for l, line in enumerate(self.ground):
                distances[p, l] = dist(point, line[0])
        # print distances
        min_indexes = np.argsort(distances, axis=1)
        min_values = [[distances[i][min_indexes[i, 0]], (i, min_indexes[i, 0])] for i in range(distances.shape[0])]
        min_values.sort(key=lambda m: m[0])
        min_dist_points = [min_values[i][1] for i in (0, 1)]
        points_on_plane = [self.ground[min_dist_points[i][1]][0] for i in (0, 1)]
        # print points_on_plane
        x0, y0, z0 = map(float, self.cp.img2world(point=points_on_plane[0],
                                                  plane=self.ground_plane,
                                                  reducing=self.reducing))
        x1, y1, z1 = map(float, self.cp.img2world(point=points_on_plane[1],
                                                  plane=self.ground_plane,
                                                  reducing=self.reducing))
        x2, y2, z2 = x0, y0, 5
        # A = np.linalg.det(np.matrix([[y1 - y0, z1 - z0], [y2 - z0, z2 - z0]]))
        # B = -np.linalg.det(np.matrix([[x1 - x0, z1 - z0], [x2 - x0, z2 - z0]]))
        # C = 0
        # D = -x0 * A - y0 * B
        p1 = np.array([x0, y0, z0])
        p2 = np.array([x1, y1, z1])
        p3 = np.array([x2, y2, z2])
        v1 = p3 - p1
        v2 = p2 - p1
        cp = np.cross(v1, v2)
        a, b, c = cp
        d = -np.dot(cp, p3)
        # print a, b, c, d
        return a, b, c, d

    def get_walls_images(self):
        self.walls_images = []
        for num, wall in enumerate(self.walls):
            img = Image3D.load(self.project, key='wall' + str(num))
            if not img:
                img = self.cp.image2plane_2(reducing=self.reducing,
                                            plane=self.define_wall_plane(wall),
                                            key='wall' + str(num),
                                            lines=wall)
            self.walls_images.append(img)

    @staticmethod
    def __load_texture(image):
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
            return texture
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
            return texture

    def __draw_ground(self):
        if not self.ground:
            return

        glBindTexture(GL_TEXTURE_2D, self.ground_texture)
        glColor3f(1, 1, 1)
        glBegin(GL_POLYGON)
        glNormal3f(0, 0, 1)
        for line in self.ground:
            _x, _y = line[0]
            wp = self.cp.img2world(point=(_x, _y),
                                   plane=self.ground_plane,
                                   reducing=self.reducing)
            tex_coord = self.ground_image.texture_coordinates(wp)
            glTexCoord2f(tex_coord[0], -tex_coord[1])
            print 'GROUND', wp, tex_coord
            glVertex3fv(wp)
        glEnd()

    def __draw_walls(self):
        for i, wall in enumerate(self.walls):
            glBindTexture(GL_TEXTURE_2D, self.walls_textures[i])
            glBegin(GL_POLYGON)
            # glColor3f(1, 1, 1)
            for line in wall:
                _x, _y = line[0]
                wp = self.cp.img2world(point=(_x, _y),
                                       plane=self.walls_planes[i],
                                       reducing=self.reducing)
                tex_coord = self.walls_images[i].texture_coordinates(wp)
                glTexCoord2f(tex_coord[0], -tex_coord[1])
                print 'WALL', wp, tex_coord
                glVertex3fv(wp)
            glEnd()

    def help_output(self):

        # # t_img = self.ground_image.image
        # for line in self.ground:
        #     wp = self.cp.img2world(line[0], (0, 0, 1, 0), self.reducing)
        #     x, y = map(int, self.ground_image.image_coordinates(wp[:2]))
        #     for i in range(x - 4, x + 5):
        #         for j in range(y - 4, y + 5):
        #             self.ground_image[i, j] = (1, 1, 0)
        # self.ground_image.image.save('DATA\\TEMP_TEXTURE.jpg')
        # exit()

        for w, wall in enumerate(self.walls):
            for line in wall:
                wp = self.cp.img2world(line[0], self.walls_planes[w], self.reducing)
                x, y = map(int, self.walls_images[w].image_coordinates(wp[:2]))
                for i in range(x - 4, x + 5):
                    for j in range(y - 4, y + 5):
                        self.walls_images[w][i, j] = (1, 1, 0)
            self.walls_images[w].image.save('DATA\\TEMP_WALL' + str(w) + '.jpg')
        exit()

        outfile = open('DATA\\LINES_OPENGL.txt', 'w')
        print '\n----OPENGL----\n'
        for line_num, line in enumerate(self.ground):
            _x, _y = line[0]
            wp = self.cp.img2world(point=(_x, _y), plane=(0, 0, 1, 0), reducing=self.reducing)
            ip = self.cp.world2img(point=wp, reducing=self.reducing)
            tex_coord = self.ground_image.texture_coordinates(wp[:2])
            print '\nN%d' % line_num
            print 'IMAGE>', (_x, _y), '--WROLD>', wp, '--IMAGE>', ip
            print '--TEXTURE>', tex_coord[0], 1 - tex_coord[1]
            print '--TEXTURE_IMAGE>', self.ground_image.image_coordinates(wp[:2]), '\n'
            outfile.write('\nN%d' % line_num)
            outfile.write('\n--IMAGE>        ' + (_x, _y).__str__())
            outfile.write('\n--WORLD>        ' + wp.__str__())
            outfile.write('\n--TEXTURE>      ' + tex_coord.__str__())
            outfile.write('\n--TEXTURE_PARAM>%d %d %d %d %f %d %d' % (wp[0],
                                                                      wp[1],
                                                                      self.ground_image.offset_x,
                                                                      self.ground_image.offset_y,
                                                                      self.ground_image.shape_reducing,
                                                                      self.ground_image.image.size[0],
                                                                      self.ground_image.image.size[1]))
            outfile.write('\n--TEXTURE_IMAGE>' + self.ground_image.image_coordinates(wp[:2]).__str__() + '\n')

        for i, wall in enumerate(self.walls):
            for line in wall:
                _x, _y = line[0]
                wp = self.cp.img2world((_x, _y), self.walls_planes[i], self.reducing)
                ip = self.cp.world2img(wp, self.reducing)
                print 'WALL', _x, _y, '->', wp, '->', ip
        outfile.close()
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

        self.ground_texture = self.__load_texture(self.ground_image.image)
        self.walls_textures = []
        for wall_image in self.walls_images:
            self.walls_textures.append(self.__load_texture(wall_image.image))

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        left, right, bottom, top, near, far = self.cp.get_internal_parameters()
        glFrustum(left, right, bottom, top, near, far)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        glRotatef(180, 1, 0, 0)
        glMultMatrixf(self.cp.get_GL_model_view_matrix())
        # print left, right, bottom, top, near, far
        # print self.cp.get_GL_model_view_matrix()
        # self.help_output()

    def __reshape(self, width, height):
        glViewport(0, 0, width, height)
        glViewport(0, 0, width, height)
        # glMatrixMode(GL_PROJECTION)
        # glLoadIdentity()
        # gluPerspective(60.0, float(width) / float(height), 1.0, 1000.0)
        glMatrixMode(GL_MODELVIEW)
        # model_view = np.zeros((4, 4))
        # model_view[:3, :] = self.cp.get_external_calibration()[:, :]
        # model_view[3, 3] = 1
        # glLoadMatrixf(model_view)
        glLoadIdentity()
        gluLookAt(self.eye[0], self.eye[1], self.eye[2],
                  self.cen[0], self.cen[1], self.cen[2],
                  self.up[0], self.up[1], self.up[2])
        # print self.eye, self.cen

    def __display(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(self.eye[0], self.eye[1], self.eye[2],
                  self.cen[0], self.cen[1], self.cen[2],
                  self.up[0], self.up[1], self.up[2])
        # self.__draw_coordinates()
        self.__draw_ground()
        self.__draw_walls()
        # exit()
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
