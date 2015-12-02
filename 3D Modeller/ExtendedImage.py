from PIL import Image
import pickle
from GUI_consts import data_path
from math import sqrt
from CommonFunctions import axis_rotation_matrix

class ExtendedImage:
    def __init__(self, image=None, offset=(0, 0), shape_reducing=1, key='ground'):
        self.image = image
        self.offset_x, self.offset_y = offset
        self.shape_reducing = shape_reducing
        self.key = key
        if self.image:
            self.pixels = self.image.load()
        self.user_texture_func = None

    def image_coordinates(self, point):
        return ((point[0] - self.offset_x) / self.shape_reducing,
                (point[1] - self.offset_y) / self.shape_reducing)

    def texture_coordinates(self, (x, y)):
        return map(lambda a, b: a / b,
                   ((x - self.offset_x) / self.shape_reducing,
                    (y - self.offset_y) / self.shape_reducing),
                   self.image.size)

    def size(self):
        return list(map(lambda a: a / self.shape_reducing, self.image.size))

    def texture_size(self):
        return self.image.size

    def __getitem__(self, item):
        if not self.image:
            raise ValueError('There\'s no image here!')
        # return self.image.getpixel((item[0] / self.shape_reducing - self.offset_x,
        #                             item[1] / self.shape_reducing - self.offset_y))
        return self.image.getpixel(self.image_coordinates(item[:2]))

    def __setitem__(self, (x, y), value):
        if not self.image:
            raise ValueError('There\'s no image here!')
        try:
            self.pixels[x, y] = value
        except IndexError:
            print self.image.size[1], self.image.size[0]
            print y, x

    def save(self, project='SOURCE'):
        source = data_path + project + '_' + self.key + '_world_image'
        self.image.save(source + '.jpg')
        with open(source + '.pick', 'wb') as f:
            pickle.dump([self.offset_x, self.offset_y, self.shape_reducing], f)

    @staticmethod
    def load(project='SOURCE', key='ground'):
        source = data_path + project + '_' + key + '_world_image'
        try:
            with open(source + '.pick', 'rb') as f:
                ox, oy, r = pickle.load(f)
            return ExtendedImage(image=Image.open(source + '.jpg'),
                                 key=key,
                                 offset=(ox, oy),
                                 shape_reducing=r)
        except IOError:
            return None

    def show(self):
        self.image.show()
