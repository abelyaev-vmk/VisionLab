from PIL import Image
import pickle
from GUI_consts import data_path
from math import sqrt, pi
from CommonFunctions import *
import numpy as np


class Image3D:
    def __init__(self, image=None, offset2=None, offset3=None, rot_matrix=None,
                 trans_scale=None, transition=None, shape_reducing=1, key='ground', use_offset=True):
        self.image = image

        self.use_offset = (offset2 or offset3) and use_offset

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

        self.rotation_matrix = rot_matrix
        self.translate_and_scale_matrix = trans_scale
        self.transition_matrix = transition
        self.key = key
        self.size = self.image.size

    def texture_coordinates(self, (x, y, z)):
        ip = self.transition_matrix * np.matrix([x, y, z, 1]).transpose()
        x, y, _ = het2hom(map(float, np.array(ip).ravel()))
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
            pickle.dump([self.offset_x, self.offset_y, self.offset_z, self.shape_reducing, self.use_offset,
                         self.key, self.rotation_matrix, self.translate_and_scale_matrix, self.transition_matrix], f)

    @staticmethod
    def load(project='SOURCE', key='ground'):
        source = data_path + project + '_' + key + '_world_image'
        try:
            with open(source + '.pick', 'rb') as f:
                ox, oy, oz, sr, uo, k, rm, tsm, tm = pickle.load(f)
            return Image3D(image=Image.open(source + '.jpg'),
                           key=key,
                           offset3=(ox, oy, oz), use_offset=uo,
                           shape_reducing=sr,
                           rot_matrix=rm, trans_scale=tsm, transition=tm)
        except IOError:
            return None

    def show(self):
        self.image.show()
