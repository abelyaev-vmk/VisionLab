import camera
from PIL import Image
from XMLParser import get_data_from_xml
import numpy as np
from math import sin, cos, tan
from os import getcwd
from os.path import isfile


class CameraProperties:
    def __init__(self, project='', location=None, quaternion=None, q_order="xyzw"):
        self.camera = camera.Camera()
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

    def get_calibration_matrix(self):
        # print 'int:\n', self.get_internal_calibration(), '\next:\n', self.get_external_calibration(), '\n'
        return self.get_internal_calibration().dot(self.get_external_calibration())

    def get_up(self):
        return self.camera.GetUp()

    def get_right(self):
        return self.camera.GetRight()

    def get_rotation_matrix(self):
        return self.camera.GetRotationMatrix()

    def get_forward(self):
        return self.camera.GetForward()

    def get_eye_center_up(self, reducing=1):
        eye = map(lambda a: a / reducing, self.get_location())
        cen = map(lambda a: a / reducing, map(lambda b, c: b + c, eye, self.get_forward()))
        up = self.get_up()
        return eye, cen, up

    def img2world(self, point=(0, 0), plane=(0, 0, 1, 0)):
        if len(point) == 2:
            point = (point[0], point[1], 1)
        matr = self.get_calibration_matrix()
        A = np.zeros((4, 4))
        A[:3, :] = matr[:, :]
        A[3, :] = plane[:]
        b = np.zeros((4, 1))
        for i in xrange(3):
            b[i] = point[i]
        b[3] = 0
        new_point = np.dot(np.linalg.inv(A), b)
        return np.array(map(lambda p: p / new_point[3], new_point[:3]))

    def world2image(self, point=(0, 0, 0)):
        pass

    def __set_xml_data(self, xml_path):
        self.xml_type, self.internal, self.external, self.geometry = get_data_from_xml(xml_path, self.xml_type)
        if self.xml_type == 1:
            self.camera.UseNonGL()
            self.camera.SetLocation(self.external['pos'])
            self.camera.SetQuaternion(self.external['rot'])
        if self.xml_type == 2:
            self.camera.UseGL()
            self.camera.SetLocation(self.external['pos'])


if __name__ == '__main__':
    cp = CameraProperties(project='SOURCE')
    # print cp.get_calibration_matrix()
    print cp.img2world(point=(2, 2), plane=(0, 0, 1, 0))
