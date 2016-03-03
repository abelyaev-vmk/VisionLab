import camera
from PIL import Image
from XMLParser import get_data_from_xml
import numpy as np
from math import sin, cos, tan, sqrt, atan2, pi
from os import getcwd
from os.path import isfile
# from ExtendedImage import ExtendedImage
from Image3D import Image3D
from CommonFunctions import *
import numpy as np
from tqdm import tqdm


class CameraProperties:
    def __init__(self, project='', location=None, quaternion=None, q_order="xyzw"):
        self.camera = camera.Camera()
        self.project = project

        if project:
            self.image = self.__find_image(project)
            xml_path = self.__find_xml(project)
            self.xml_type = -1
            if xml_path:
                self.__set_xml_data(xml_path)
        elif location:
            self.camera.SetLocation(location)
            self.camera.SetQuaternion(quaternion)
        else:
            raise AttributeError('Not enough arguments')
        self.calibration_matrix = self.get_calibration_matrix()

    @staticmethod
    def __find_image(project):
        if isfile(getcwd() + '//' + project + '.jpg'):
            return Image.open(project + '.jpg')
        elif isfile(getcwd() + '//' + project + 'png'):
            return Image.open(project + 'png')
        else:
            return None

    @staticmethod
    def __find_xml(project):
        if isfile(getcwd() + '//' + project + '.xml'):
            return project + '.xml'
        else:
            return ''

    def __set_xml_data(self, xml_path):
        self.xml_type, self.internal, self.external, self.geometry = \
            get_data_from_xml(xml_path, self.xml_type)

        if self.xml_type == 1:
            self.camera.UseNonGL()
            # self.camera.UseGL()
            self.camera.SetLocation(self.external['pos'])
            self.camera.SetQuaternion(self.external['rot'])

        if self.xml_type == 2:
            self.camera.UseGL()
            self.camera.SetLocation(self.external['pos'])

    @staticmethod
    def make_project_name(path):
        if '.' not in path:
            return path
        else:
            return path[:path.find('.')]

    def get_location(self):
        return self.camera.GetLocation()

    def get_quaternion(self):
        return self.camera.GetQuaternion()

    def get_external_calibration(self):
        if self.xml_type == 2:
            rx, ry, rz = self.external['rot']
            tx, ty, tz = self.external['pos']
            sa, ca, sb, cb, sg, cg = sin(rx), cos(rx), sin(ry), cos(ry), sin(rz), cos(rz)
            matr = np.array([[cb * cg, cb * sg, -sb],
                             [cg * sa * sb - ca * sg, sa * sb * sg + ca * cg, cb * sa],
                             [sa * sg + ca * cg * sb, ca * sb * sg - cg * sa, ca * cb],
                             [tx, ty, tz]]).transpose()
            return matr
        else:
            return self.camera.GetViewMatrix()

    def get_external_calibration_v2(self):
        if self.xml_type == 1:
            return self.get_GL_model_view_matrix()
        if self.xml_type == 2:
            rx, ry, rz = self.external['rot']
            tx, ty, tz = self.external['pos']
            sx, cx, sy, cy, sz, cz = sin(rx), cos(rx), sin(ry), cos(ry), sin(rz), cos(rz)
            Rx = np.matrix([[1, 0, 0, 0], [0, cx, sx, 0], [0, -sx, cx, 0], [0, 0, 0, 1]])
            Ry = np.matrix([[cy, 0, sy, 0], [0, 1, 0, 0], [-sy, 0, cy, 0], [0, 0, 0, 1]])
            Rz = np.matrix([[cz, sz, 0, 0], [-sz, cz, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
            R = Rx * Ry * Rz
            matr = np.matrix(np.zeros((4, 4)))
            matr[:3, :3] = R[:3, :3]
            matr[0, 3] = tx
            matr[1, 3] = ty
            matr[2, 3] = tz
            matr[3, 3] = 1
            return matr

    def get_internal_calibration(self):
        if not self.xml_type:
            raise ValueError('Have no information about camera')
        elif self.xml_type == 1:
            fl, pp, s = self.internal['fl'], self.internal['pp'], self.internal['s']
            return np.array([[fl[0], tan(s) * fl[1], pp[0]],
                             [0, fl[1], pp[1]],
                             [0, 0, 1]])
        elif self.xml_type == 2:
            matr = np.zeros((3, 3))
            matr[0, 0] = self.internal['sx'] / self.geometry['dp'][0]
            matr[0, 2] = self.internal['c'][0]
            matr[1, 1] = 1 / self.geometry['dp'][1]
            matr[1, 2] = self.internal['c'][1]
            matr[2, 2] = 1
            return np.dot(matr, np.array([[self.internal['focal'], 0, 0],
                                          [0, self.internal['focal'], 0],
                                          [0, 0, 1]]))

    def get_internal_parameters(self):
        f = np.mean(self.internal['fl' if self.xml_type == 1 else 'focal'])
        cx, cy = self.internal['pp' if self.xml_type == 1 else 'c']
        pixel_center_offset = 0.5
        near = 1.0
        far = 1e2
        width, height = self.image.size
        right = (width - (cx + pixel_center_offset)) * (near / f)
        left = - (cx + pixel_center_offset) * (near / f)
        top = - (height - (cy + pixel_center_offset)) * (near / f)
        bottom = (cy + pixel_center_offset) * (near / f)
        return left, right, bottom, top, near, far

    def get_GL_projection_matrix(self):
        l, r, b, t, n, f = self.get_internal_parameters()
        return np.matrix([[2 * n / (r - l), 0, (r + l) / (r - l), 0],
                          [0, 2 * n / (t - b), (t + b) / (t - b), 0],
                          [0, 0, -(f + n) / (f - n), -2 * f * n / (f - n)],
                          [0, 0, -1, 0]])

    def get_GL_model_view_matrix(self):
        view_matrix = self.get_external_calibration()
        gl_view_matrix = np.asarray(np.vstack((view_matrix, np.array([0, 0, 0, 1]))), np.float32, order='F')
        return gl_view_matrix

    def get_calibration_matrix(self):
        # print 'int:\n', self.get_internal_calibration(), '\next:\n', self.get_external_calibration(), '\n'
        return np.matrix(self.get_internal_calibration()) * np.matrix(self.get_external_calibration())

    def get_calibration_matrix_v2(self):
        # http://cgm.computergraphics.ru/content/view/34
        K = np.matrix(self.get_internal_calibration())
        Ip = np.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0]])
        G = np.matrix(self.get_external_calibration_v2())
        return K * Ip * G

    def get_up(self):
        return self.camera.GetUp()

    def get_right(self):
        return self.camera.GetRight()

    def get_rotation_matrix(self):
        return self.camera.GetRotationMatrix()

    def get_forward(self):
        return self.camera.GetForward()

    def get_eye_center_up_right(self, reducing=1):
        eye = map(lambda a: a / reducing, self.get_location())
        cen = map(lambda b, c: b + c, eye, self.get_forward())
        up = self.get_up()
        right = self.get_right()
        return eye, cen, up, right

    def img2world(self, point=(0, 0), plane=(0, 0, 1, 0), reducing=1):
        if len(point) == 2:
            point = (point[0], point[1], 1)
        matr = self.calibration_matrix
        A = np.zeros((4, 4))
        A[:3, :] = matr[:, :]
        A[3, :] = plane[:]
        b = np.zeros((4, 1))
        for i in xrange(3):
            b[i] = point[i]
        b[3] = 0
        new_point = np.dot(np.linalg.inv(A), b)
        return np.array(map(lambda p: p / new_point[3] / reducing, new_point[:3]))

    def world2img(self, point=(0, 0, 0), reducing=1):
        point = map(lambda p: p * reducing, point[:3]) + [1]
        image_point = self.get_calibration_matrix().dot(point)
        # print 'IP', image_point, image_point[0, 0]
        imp = [image_point[0, 0] / image_point[0, 2], image_point[0, 1] / image_point[0, 2]]
        # print imp
        return imp
        # return np.array(map(lambda p: p / image_point[2], image_point[:2]))

    def interpolate(self, in_point=(0, 0)):
        point = in_point if len(in_point) == 2 else in_point[:2]
        x, y = map(int, point)
        near_points = [[x, y]]
        if x > 0:
            near_points.append([x - 1, y])
        if x < self.image.size[0] - 1:
            near_points.append([x + 1, y])
        if y > 1:
            near_points.append([x, y - 1])
        if y < self.image.size[1]:
            near_points.append([x, y + 1])
        distances = np.array([1 - sqrt((x - nearp[0]) ** 2 + (y - nearp[1]) ** 2)
                              for nearp in near_points])
        distances /= sum(distances)
        try:
            pixels = [self.image.getpixel((nearp[0], self.image.size[1] - nearp[1])) for nearp in near_points]
        except IndexError:
            # print "INDEX ERROR!"
            # print "POINT =", point
            # print "NEARS =", near_points
            # print "DISTS =", distances
            return 0, 0, 0, 255
        # print distances, pixels
        color = [sum([pixels[i][j] * d for i, d in enumerate(distances)]) for j in range(4)]
        return tuple(map(int, color))

    def image2plane_v2(self, reducing=1, max_size=750, plane=(0, 0, 1, 0), key='ground', lines=()):
        if lines is None:
            return
        # # CORNERS IN WORLD
        # print lines
        # for i in range(lines.__len__()):
        #     for j in range(2):
        #         lines[i][j][1] = self.image.size[1] - lines[i][j][1]

        self.calibration_matrix = self.get_calibration_matrix()

        corners = map(lambda p: self.img2world(point=p, plane=plane, reducing=reducing),
                      ((0, 0),
                       (self.image.size[0] - 1, 0),
                       (0, self.image.size[1] - 1),
                       (self.image.size[0] - 1, self.image.size[1] - 1)))
        # corners = map(lambda p: self.img2world(point=p, plane=plane, reducing=reducing), lines)

        # # # OFFSET on 3D

        img_lines = map(lambda p:
                        self.img2world(point=p,
                                       plane=plane, reducing=reducing), [line[0] for line in lines])
        min_coord = img_lines[0]
        max_coord = min_coord.copy()
        for line in img_lines:
            min_coord = map(min, min_coord, line)
            max_coord = map(max, max_coord, line)
        offset = map(float, min_coord[:2])
        # offset = (0, 0, 0)
        translation_3D = translate_and_scale_matrix((-offset[0], -offset[1], 0), 1)
        print 'LINES1:', img_lines
        img_lines = map(lambda p: het2hom(translation_3D * np.matrix(hom2het(p)).transpose()), img_lines)
        print 'LINES2:', img_lines

        # # # ROTATION !!!!!!

        axis = ground_axis(img_lines)

        print 'axis:', axis
        rot_matrix = hom2het(matrix=axis_rotation_matrix(axis, pi / 2 if key[:4] == 'wall' else 0))

        # # # OFFSET on 2D
        corners = map(lambda c: het2hom(vector=rot_matrix * translation_3D * np.matrix(hom2het(vector=c)).transpose()), corners)
        print 'CORNERS:', corners
        min_coord = corners[0]
        max_coord = min_coord.copy()
        for corner in corners:
            min_coord = map(min, min_coord, corner)
            max_coord = map(max, max_coord, corner)
        offset = map(float, min_coord[:2])

        # # # SHAPE
        shape = map(lambda m, o: m - o, max_coord[:2], offset[:2])
        shape_reducing = float(max(shape[0] / max_size, shape[1] / max_size))
        shape = map(lambda s: int(s / shape_reducing), shape)

        # # # TRANSLATION AND SCALE
        print '\nSHAPE', shape_reducing, '\n'
        translation_and_scale_matrix = translate_and_scale_matrix((-offset[0], -offset[1], 0), 1 / shape_reducing)

        print lines[0][0]
        print hom2het(lines[0][0])

        # # # TRANSITION
        transition_matrix = translation_and_scale_matrix * rot_matrix * translation_3D
        inv_transition_matrix = np.linalg.inv(transition_matrix)

        img = Image3D(image=Image.new("RGBA", shape, "white"), shape_reducing=shape_reducing, key=key,
                      transition=transition_matrix)
        outfile = open('DATA\\LINES_VER2_%s.txt' % key, 'w')
        writed = [0 for _ in xrange(len(lines))]

        for ix in range(shape[0]):
            for iy in range(shape[1]):

                wp = inv_transition_matrix * np.matrix(hom2het(vector=[ix, iy, 0])).transpose()
                wx, wy, wz = np.array(het2hom(wp)).ravel()
                point = self.world2img(point=(wx, wy, wz), reducing=reducing)
                if not all(0 <= point[i] < self.image.size[i] for i in (0, 1)):
                    continue
                for line_num, line in enumerate(lines):
                    world_point = wx, wy, wz
                    if all(abs(point[i] - line[0][i]) <= 5 for i in (0, 1)) and not writed[line_num]:
                        outfile.write('\n\nN%d' % line_num)
                        outfile.write('\n--IMAGE>        ' + point[:2].__str__())
                        outfile.write('\n--WORLD>        ' + world_point.__str__())
                        outfile.write('\n--TEXTURE>      ' + img.texture_coordinates(world_point).__str__())
                        outfile.write('\n--TEXTURE_IMAGE>' + (ix, iy).__str__())
                        writed[line_num] = 1

                # img[ix, iy] = self.image.getpixel((int(point[0]), int(self.image.size[1] - point[1])))
                temp_change = lambda poi: (int(point[0]), self.image.size[1] - int(point[1]) - 1)
                # temp_change = lambda poi: poi

                img[ix, iy] = self.interpolate(temp_change(point))
            if ix in (i * shape[0] / 20 for i in range(0, 20)):
                print "Done %d / %d" % (ix, shape[0])
        outfile.close()
        img.save(project=self.project)
        img.show()

        return img

    def help_function(self):
        img = Image.new("RGBA", self.image.size, 'white')
        w, h = img.size
        pixels = img.load()
        pixels[0, 0] = (1, 1, 0)
        img.save('TEMPIMG.jpg')
        exit(0)




if __name__ == '__main__':
    cp = CameraProperties(project='SOURCE-2')
    # print cp.get_calibration_matrix()
    w = cp.img2world(point=(2, 2), plane=(0, 0, 1, 0))
    # print w
    # print cp.world2image(point=w)
    cp.image2plane_v2(reducing=1)
