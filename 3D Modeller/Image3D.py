from PIL import Image
import pickle
from GUI_consts import data_path
from math import sqrt, pi
from CommonFunctions import axis_rotation_matrix
import numpy as np


class Image3D:
    def __init__(self, image=None, offset2=None, offset3=None, axis=None, shape_reducing=1, key='ground'):
        self.image = image

        if offset2:
            self.offset_x, self.offset_y = offset2
            self.offset_z = 0
        elif offset3:
            self.offset_x, self.offset_y, self.offset_z = offset3
        else:
            self.offset_x, self.offset_y, self.offset_z = 0, 0, 0

        self.shape_reducing = shape_reducing
        if self.image:
            self.pixels = self.image.load()
        else:
            self.pixels = None

        if axis:
            self.axis = axis
            self.rotation_matrix = axis_rotation_matrix(axis, pi / 2)
        else:
            self.axis, self.rotation_matrix = None, None
        self.key = key
        self.size = self.image.size

    def texture_coordinates(self, (x, y, z)):
        if not self.axis:
            x, y, z = (x - self.offset_x) / self.shape_reducing, \
                      (y - self.offset_y) / self.shape_reducing, \
                      (z - self.offset_z) / self.shape_reducing
            tex_x, tex_y = sqrt(x ** 2 + z ** 2), y
            return map(lambda a, b: a / b, (tex_x, tex_y), self.size)
        else:
            x, y, z = (x - self.offset_x) / self.shape_reducing, \
                      (y - self.offset_y) / self.shape_reducing, \
                      (z - self.offset_z) / self.shape_reducing
            # noinspection PyTypeChecker
            x, y, z = np.dot(self.rotation_matrix, np.asarray([x, y, z]))
            return map(lambda a, b: a / b, (x, y), self.size)

    def __setitem__(self, (x, y), value):
        if not self.image:
            raise ValueError('There\'s no image here!')
        try:
            self.pixels[x, y] = value
        except IndexError:
            print self.image.size[1], self.image.size[0]
            print y, x
            print 'INDEX ERROR'
            exit()

    def save(self, project='SOURCE'):
        source = data_path + project + '_' + self.key + '_world_image'
        self.image.save(source + '.jpg')
        with open(source + '.pick', 'wb') as f:
            pickle.dump([self.offset_x, self.offset_y, self.offset_z, self.shape_reducing], f)

    @staticmethod
    def load(project='SOURCE', key='ground'):
        source = data_path + project + '_' + key + '_world_image'
        try:
            with open(source + '.pick', 'rb') as f:
                ox, oy, oz, r = pickle.load(f)
            return Image3D(image=Image.open(source + '.jpg'),
                                 key=key,
                                 offset3=(ox, oy, oz),
                                 shape_reducing=r)
        except IOError:
            return None

    def show(self):
        self.image.show()
